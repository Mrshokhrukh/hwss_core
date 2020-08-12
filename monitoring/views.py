import json
import logging
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Prefetch, Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from access.models import Agency, CustomUser, UserAgency
from gyalsung_users.models import GyalsungUserProfile
from measurement.models import (
    Measurement,
    MeasurementAssist,
    Submission,
    UserSubmission,
)
from monitoring.models import (
    FinalUserSubmission,
    Notification,
    Referral,
    Rescreening,
    ServiceAndTreatment,
    ServiceAndTreatmentHistory,
    Substance,
    SubstanceRiskMeasurement,
)
from monitoring.serializers import (
    FinalUserSubmissionSerializer,
    ReferralSerializer,
    ServiceAndTreatmentSerializer,
)
from screening.models import (
    CaseBasedSubmission,
    CaseScreening,
    EventBasedSubmission,
    EventScreening,
)

logger = logging.getLogger(__name__)


method_decorator(csrf_exempt, name="dispatch")


class ServiceAndTreatmentViewSet(viewsets.ModelViewSet):
    queryset = ServiceAndTreatment.objects.all()
    serializer_class = ServiceAndTreatmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ServiceAndTreatment.objects.all().select_related(
            "content_type",
            "user",
            "user__active_agency",
            "user__agency_details",
            "updated_by",
            "updated_by__active_agency",
        )

    @action(detail=False, methods=["get"], url_path="get-service-and-treatment")
    def get_service_and_treatment(self, request):
        response = create_service_and_treatments(request)

        if response.get("status") == "error":
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        # optimized for the generic foreign key

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@csrf_exempt
def submit_rescreening(request):
    if request.method == "POST":
        user_id = request.POST.get("userId")
        rescreened_by_id = request.POST.get("rescreened_by")

        user = get_object_or_404(CustomUser, id=user_id)
        rescreened_by_user = get_object_or_404(CustomUser, id=rescreened_by_id)

        age = calculate_age(user.date_of_birth)

        assist_data_json = request.POST.get("assistRiskSeverity", "{}")
        assist_data = json.loads(assist_data_json) if assist_data_json else {}

        gad_data_json = request.POST.get("gadData", "{}")
        gad_data = json.loads(gad_data_json) if gad_data_json else {}
        gad_score = gad_data.get("totalScore", 0)
        gad_interpretation = gad_data.get("interpretation", "")

        phq_data_json = request.POST.get("phqData", "{}")
        phq_data = json.loads(phq_data_json) if phq_data_json else {}
        phq_score = phq_data.get("totalScore", 0)
        phq_interpretation = phq_data.get("interpretation", "")

        ace_data_json = request.POST.get("aceData", "{}")
        ace_data = json.loads(ace_data_json) if ace_data_json else {}
        ace_score = ace_data.get("totalScore", 0)
        ace_interpretation = ace_data.get("interpretation", "")

        with transaction.atomic():
            rescreening, created = Rescreening.objects.update_or_create(
                user=user,
                defaults={
                    "gad_data": gad_data_json,
                    "gad_score": gad_score,
                    "gad_interpretation": gad_interpretation,
                    "phq_data": phq_data_json,
                    "phq_score": phq_score,
                    "phq_interpretation": phq_interpretation,
                    "ace_data": ace_data_json,
                    "ace_score": ace_score,
                    "ace_interpretation": ace_interpretation,
                    "school_env_data": request.POST.get("schoolEnvData", "{}"),
                    "rescreened": True,
                    "screened_by": rescreened_by_user,
                    "rescreening_date": timezone.now(),
                },
            )

            # Save substance risk measurements
            for substance, risk_level in assist_data.items():
                # Extract risk flag (first word of risk_level)
                risk_flag = risk_level.split()[0]

                # Safely extract total_score
                try:
                    total_score = risk_level.split("(")[1].split(")")[0]
                    total_score = float(total_score)  # Convert to float
                except (IndexError, ValueError):  # Handle cases where parsing fails
                    total_score = (
                        0.0  # Default to 0.0 if score is not available or malformed
                    )

                # Create or update substance risk measurement
                substance_instance, _ = Substance.objects.get_or_create(name=substance)

                SubstanceRiskMeasurement.objects.create(
                    substance=substance_instance,
                    rescreening=rescreening,
                    measurement=total_score,
                    risk_flag=risk_flag,
                )

            # Set the rescreened field of the associated UserSubmission to True
            user_submission = UserSubmission.objects.get(user=user)
            user_submission.rescreened = True
            user_submission.save()

        # Return appropriate message depending on whether the rescreening was created or updated
        message = (
            "Rescreening data saved successfully."
            if created
            else "Rescreening data updated successfully."
        )

        return JsonResponse({"message": message})

    else:
        return JsonResponse({"error": "Only POST requests are allowed."})


def get_non_green_flags(request):
    rescreening_list = []

    # Iterate over all UserSubmission instances
    for submission in UserSubmission.objects.filter(
        rescreened=False, mark_as_safe=False
    ):
        # Initialize a dictionary to store data for the current submission
        submission_data = {
            "submission_id": submission.id,
            "flags": {},  # Initialize flags dictionary
            "user_details": {},
            "measurement_data": {},
            "measurement_assist_data": {},
            "user_agency_data": {},
            "diagnosis": "",  # Initialize diagnosis field
        }

        # Fetch Measurement and MeasurementAssist instances for the current submission
        measurement = Measurement.objects.filter(user_submission=submission).first()
        measurement_assist = MeasurementAssist.objects.filter(
            user_submission=submission
        ).first()

        # Fetch Submission details for the submission
        submission_details = Submission.objects.filter(
            user_submission=submission
        ).first()
        if submission_details:
            submission_data["diagnosis"] = submission_details.diagnosis
            submission_data["created_at"] = submission_details.created_at

        # Fetch user details for the submission
        middle_name = submission.user.middle_name if submission.user.middle_name else ""
        full_name = f"{submission.user.first_name} {middle_name} {submission.user.last_name}".strip()
        user_details = {
            "full_name": full_name,
            "age": calculate_age(submission.user.date_of_birth),
            "sex": submission.user.gender,
            "user_id": submission.user.id,
        }
        submission_data["user_details"] = user_details

        # Fetch user agency details for the submission
        if submission.user.active_agency:
            user_agency_data = {}
            try:
                user_agency = submission.user.agency_details
                user_agency_data = {
                    "agency_name": user_agency.agency.agency_name,
                    "user_role_agency": user_agency.user_role_agency,
                    "user_class": user_agency.user_class,
                    "user_stream": user_agency.user_stream,
                    "user_sub_class": user_agency.user_sub_class,
                    "user_dzongkhag": submission.user.active_agency.present_dzongkhag,
                }
            except UserAgency.DoesNotExist:
                user_agency_data = {}
            submission_data["user_agency_data"] = user_agency_data

        # Check MeasurementAssist flags
        if measurement_assist:
            for field in measurement_assist._meta.fields:
                if field.name.endswith("_flag"):
                    flag_value = getattr(measurement_assist, field.name)
                    if flag_value != "green":
                        submission_data["flags"][field.name] = flag_value

        if measurement:
            for field in measurement._meta.fields:
                if field.name.endswith("_flag"):
                    flag_value = getattr(measurement, field.name)
                    if flag_value != "green":
                        submission_data["flags"][field.name] = flag_value

        if submission_data["flags"]:
            if measurement:
                submission_data["measurement_data"] = model_to_dict(measurement)
            if measurement_assist:
                submission_data["measurement_assist_data"] = model_to_dict(
                    measurement_assist
                )
            rescreening_list.append(submission_data)

    return {"Rescreening List": rescreening_list}


@csrf_exempt
def process_rescreening(request):
    rescreening_records = get_non_green_flags(request)

    # Log the data being returned
    logger.debug("Response data:")
    logger.debug(rescreening_records)

    return JsonResponse(rescreening_records)


def calculate_age(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age


def get_user_details(user):
    user_agency = UserAgency.objects.filter(user=user).first()
    agency_details = None
    if user_agency:
        agency_details = {
            "agency_name": user_agency.agency.agency_name,
            "agency_code": user_agency.agency.agency_code,
            "parent_occupation": user_agency.parent_occupation,
            "parent_status": user_agency.parent_status,
        }
    return {
        "id": user.id,
        "full_name": f"{user.first_name} {user.middle_name or ''} {user.last_name}",
        "age": (timezone.now().date() - user.date_of_birth).days // 365,
        "gender": user.gender,
        "user_agency": agency_details,
    }


def generateServiceAndTreatment(request):
    try:
        rescreenings = Rescreening.objects.all()

        existing_service_and_treatments = ServiceAndTreatment.objects.filter(
            user__in=[res.user for res in rescreenings],
            date__in=[
                res.submission_date.date()
                for res in rescreenings
                if res.submission_date
            ],
        ).values_list("user", "date")

        new_service_and_treatments = []
        for rescreening in rescreenings:
            if (
                rescreening.submission_date
                and (rescreening.user, rescreening.submission_date.date())
                not in existing_service_and_treatments
            ):
                new_service_and_treatments.append(
                    ServiceAndTreatment(
                        user=rescreening.user,
                        date=rescreening.submission_date.date(),
                        assessment_status="Not Conducted",
                        case_status="On Going",
                        counseling="Waiting List",
                        rescreened=True,
                        follow_up="",
                        comments="",
                    )
                )
                rescreening.rescreened = True

        ServiceAndTreatment.objects.bulk_create(new_service_and_treatments)
        Rescreening.objects.bulk_update(rescreenings, ["rescreened"])

        case_screenings = CaseScreening.objects.all()
        case_based_submissions = CaseBasedSubmission.objects.filter(
            case__in=case_screenings
        )

        event_screenings = EventScreening.objects.all()
        event_based_submissions = EventBasedSubmission.objects.filter(
            event__in=event_screenings
        )

        service_and_treatments_data = [
            {
                "user": get_user_details(obj.user),
                "date": obj.date,
                "assessment_status": obj.assessment_status,
                "case_status": obj.case_status,
                "counseling": obj.counseling,
                "follow_up": obj.follow_up,
                "comments": obj.comments,
            }
            for obj in ServiceAndTreatment.objects.all()
        ]

        case_screening_data = [
            {
                "user": get_user_details(case.user),
                "case_name": case.case_name,
                "purpose": case.purpose,
                "date": case.date,
                "dzongkhag": case.dzongkhag,
                "counselor": case.counselor,
            }
            for case in case_screenings
        ]

        case_based_submission_data = [
            {
                "user": get_user_details(sub.user),
                "case_name": sub.case.case_name,
                "gad_score": sub.gad_score,
                "phq_score": sub.phq_score,
                "ace_score": sub.ace_score,
            }
            for sub in case_based_submissions
        ]

        # Formatting EventScreening and EventBasedSubmission data
        event_screening_data = [
            {
                "event_name": event.event_name,
                "location": event.location,
                "counselor": event.counselor,
                "start_date": event.start_date,
                "end_date": event.end_date,
            }
            for event in event_screenings
        ]

        event_based_submission_data = [
            {
                "user": get_user_details(sub.user),
                "event_name": sub.event.event_name,
                "gad_score": sub.gad_score,
                "phq_score": sub.phq_score,
                "ace_score": sub.ace_score,
            }
            for sub in event_based_submissions
        ]

        # Fetching counselor data (optimized)
        counselors = CustomUser.objects.exclude(
            Q(role__in=["student", "public"]) | Q(role__contains="_admin")
        ).values(
            "first_name",
            "middle_name",
            "last_name",
            "active_agency__agency_name",
            "role",
        )

        # Returning combined JSON response
        return JsonResponse(
            {
                "message": "ServiceAndTreatment, CaseScreening, and EventScreening records updated successfully",
                "service_and_treatments_data": service_and_treatments_data,
                "case_screening_data": case_screening_data,
                "case_based_submission_data": case_based_submission_data,
                "event_screening_data": event_screening_data,
                "event_based_submission_data": event_based_submission_data,
                "counselors": list(counselors),
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.error(f"Error in generateServiceAndTreatment: {e}")
        return JsonResponse(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@csrf_exempt
@require_POST
def update_service_and_treatment(request):
    if request.method == "POST":
        try:
            # Get the update data from the request body
            data = json.loads(request.body)
            update_data = data.get("updateData")

            custom_user_id = update_data.get("id")
            service_and_treatments = ServiceAndTreatment.objects.filter(
                user_id=custom_user_id
            )

            # Check if any ServiceAndTreatment instance is found
            if not service_and_treatments.exists():
                error_msg = "ServiceAndTreatment not found for user_id: {}".format(
                    custom_user_id
                )
                return JsonResponse({"error": error_msg}, status.HTTP_404_NOT_FOUND)

            # Get the counselor's CustomUser instance
            counselor_id = update_data.get("updated_by")
            counselor = get_user_model().objects.get(id=counselor_id)

            for service_and_treatment in service_and_treatments:
                history_entry = ServiceAndTreatmentHistory.objects.create(
                    service_and_treatment=service_and_treatment,
                    updated_by=counselor,
                    updated_at=timezone.now(),
                    changes=json.dumps(update_data),
                )
                history_entry.save()

                # Update the ServiceAndTreatment instance with the latest data
                service_and_treatment.assessment_status = update_data.get(
                    "assessment_status"
                )
                service_and_treatment.case_status = update_data.get("case_status")
                service_and_treatment.counseling = update_data.get("counseling")
                service_and_treatment.follow_up = update_data.get("follow_up")
                service_and_treatment.comments = update_data.get("comments")
                service_and_treatment.updated_by = counselor

                service_and_treatment.save()

            # Return success response
            return JsonResponse(
                {"message": "ServiceAndTreatment updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            return JsonResponse(
                {"error": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return JsonResponse(
            {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@csrf_exempt
def getReferralList(request):
    referrals = (
        Referral.objects.all()
        .select_related("user", "referred_by", "referred_to")
        .prefetch_related(
            Prefetch(
                "service_and_treatment",
                queryset=ServiceAndTreatment.objects.select_related("user"),
            )
        )
    )

    referral_list = []

    for referral in referrals:
        birth_date = referral.user.date_of_birth
        age = calculate_age(birth_date)

        user_data = {
            "date_of_birth": birth_date.strftime("%Y-%m-%d"),
            "name": f"{referral.user.first_name} {referral.user.middle_name} {referral.user.last_name}",
            "age": age,
            "gender": referral.user.gender,
            "patient_id": referral.user.id,
        }

        referral_data = {
            "user_data": user_data,
            "referred_by": {
                "username": (
                    referral.referred_by.username if referral.referred_by else None
                )
            },
            "referred_to": {
                "name": referral.referred_to_name,
                "user_id": referral.referred_to_id,
            },
            "date": referral.date,
            "referral_status": referral.referral_status,
            "referral_remarks": referral.referral_remarks,
            # Include details from ServiceAndTreatment model
            "assessment_status": (
                referral.service_and_treatment.assessment_status
                if referral.service_and_treatment
                else None
            ),
            "counseling_status": (
                referral.service_and_treatment.counseling
                if referral.service_and_treatment
                else None
            ),
            "follow_up": (
                referral.service_and_treatment.follow_up
                if referral.service_and_treatment
                else None
            ),
            "comments": (
                referral.service_and_treatment.comments
                if referral.service_and_treatment
                else None
            ),
        }
        referral_list.append(referral_data)

    return JsonResponse({"referral_list": referral_list}, status=status.HTTP_200_OK)


@csrf_exempt
def update_referral_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            refer_data = data.get("referData")

            if not refer_data:
                return JsonResponse(
                    {"error": "No referral data provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            referred_by_id = refer_data.get("referred_by")
            referred_to_info = refer_data.get(
                "referred_to_name"
            )  # Changed to referred_to_info to reflect it is a dictionary
            user_id = refer_data.get("user")

            if not all([referred_by_id, referred_to_info, user_id]):
                return JsonResponse(
                    {
                        "error": f"Incomplete data provided. Got: referred_by={referred_by_id}, "
                        f"referred_to_name={referred_to_info}, user_id={user_id}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            referred_by = CustomUser.objects.get(id=referred_by_id)

            # Extract `id` or other relevant fields from the referred_to_info dictionary
            referred_to_id = referred_to_info.get("id")
            referred_to_full_name = referred_to_info.get("full_name")

            if not referred_to_id:
                return JsonResponse(
                    {"error": "Referred to user ID is missing in referred_to_name."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            referred_to = CustomUser.objects.get(id=referred_to_id)

            with transaction.atomic():
                service_and_treatment = ServiceAndTreatment.objects.filter(
                    user_id=user_id
                ).first()
                if not service_and_treatment:
                    return JsonResponse(
                        {
                            "error": f"No service and treatment record found for user ID {user_id}."
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                content_type = ContentType.objects.get_for_model(ServiceAndTreatment)

                referral, created = Referral.objects.update_or_create(
                    user_id=user_id,
                    defaults={
                        "referred_by": referred_by,
                        "referred_to": referred_to,
                        "referred_to_name": referred_to_full_name,  # Save full_name for reference
                        "referral_status": "Awaiting",
                        "date": timezone.now(),
                        "service_and_treatment": service_and_treatment,
                        "content_type": content_type,
                        "object_id": service_and_treatment.id,
                    },
                )

                # Update the service and treatment record
                service_and_treatment.referred = "Referred"
                service_and_treatment.referral_instance = referral
                service_and_treatment.save()

                # Send email to the referred_to user
                send_mail(
                    subject="New Referral Notification",
                    message=f"Dear {referred_to_full_name},\n\n"
                    f"A new case has been referred by {referred_by.first_name} {referred_by.last_name} to you.\n\n"
                    f"Please log in to the system to review the referral.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[referred_to.email],
                    fail_silently=False,
                )

                # Create notification for referred_to user
                Notification.objects.create(
                    notification_for=referred_to,
                    notification=f"A new referral has been assigned to you by {referred_by.first_name} {referred_by.last_name}.",
                )

                return JsonResponse(
                    {
                        "message": "Referral saved successfully!",
                        "referral_id": referral.id,
                    },
                    status=status.HTTP_200_OK,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback

            return JsonResponse(
                {
                    "error": f"An error occurred: {str(e)}",
                    "traceback": traceback.format_exc(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return JsonResponse(
        {"error": "Only POST requests are allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


# function for getting users details:
def get_user_monitoring_details(request):
    user_id = request.GET.get("user_id")

    if user_id is None:
        return JsonResponse(
            {"error": "User ID is missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = get_object_or_404(CustomUser, pk=user_id)

    try:
        user_agency = UserAgency.objects.get(user=user)
        agency_details = {
            "agency_name": user_agency.agency.agency_name,
            "agency_code": user_agency.agency.agency_code,
            "agency_parent": user_agency.agency.agency_parent,
            "parent_occupation": user_agency.parent_occupation,
            "parent_status": user_agency.parent_status,
        }
    except UserAgency.DoesNotExist:
        agency_details = None

    agency_active_details = []
    if user.active_agency:
        agency_active_details.append(
            {
                "present_dzongkhag": user.active_agency.present_dzongkhag,
                "present_gewog": user.active_agency.present_gewog,
                "present_village": user.active_agency.present_village,
            }
        )

    service_and_treatment_details = list(
        ServiceAndTreatment.objects.filter(user=user).values()
    )

    referral_details = list(Referral.objects.filter(user=user).values())

    user_submissions = UserSubmission.objects.filter(user=user)
    diagnosis_details = list(
        Submission.objects.filter(user_submission__in=user_submissions).values(
            "diagnosis"
        )
    )

    rescreenings = Rescreening.objects.filter(user=user)
    rescreening_details = []
    for rescreening in rescreenings:
        rescreening_data = {
            "id": rescreening.id,
            "submission_date": rescreening.submission_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        rescreening_details.append(rescreening_data)

    substance_risk_measurements = SubstanceRiskMeasurement.objects.filter(
        rescreening__in=rescreenings
    )
    substance_risk_measurement_details = []
    for measurement in substance_risk_measurements:
        substance_name = measurement.substance.name
        measurement_data = {
            "id": measurement.id,
            "substance_name": substance_name,
            "measurement": measurement.measurement,
            "risk_flag": measurement.risk_flag,
            "total_score": measurement.total_score,
        }
        substance_risk_measurement_details.append(measurement_data)

    user_details = {
        "id": user.id,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "identity_number": user.identity_number,
        "nationality": user.nationality,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d"),
        "gender": user.gender,
        "email": user.email,
        "mob_number": user.mob_number,
        "father_name": user.father_name,
        "mother_name": user.mother_name,
        "perm_add_village": user.perm_add_village,
        "perm_add_gewog": user.perm_add_gewog,
        "perm_add_dzongkhag": user.perm_add_dzongkhag,
        "profile_picture": user.profile_picture.url if user.profile_picture else None,
        "active_agency": user.active_agency.agency_name if user.active_agency else None,
        "ps_add_village": user.ps_add_village,
        "ps_add_gewog": user.ps_add_gewog,
        "ps_add_dzongkhag": user.ps_add_dzongkhag,
        "is_gyalsung": user.is_gyalsung,
        "academy_code": user.academy_code,
        "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        "role": user.role,
        "access_level": user.access_level,
        "agency_details": agency_details,
        "service_and_treatment_details": service_and_treatment_details,
        "referral_details": referral_details,
        "rescreening_details": rescreening_details,
        "substance_risk_measurement_details": substance_risk_measurement_details,
        "agency": agency_active_details,
        "diagnosis_details": diagnosis_details,
    }

    return JsonResponse(user_details)


@csrf_exempt
def accept_referral(request):
    if request.method == "POST":
        data = json.loads(request.body)
        referred_to_user_id = data.get("referredToUserId")
        patient_id = data.get("patientId")

        referred_counselor = get_object_or_404(CustomUser, id=referred_to_user_id)
        referred_patient = get_object_or_404(CustomUser, id=patient_id)

        try:
            referral = Referral.objects.filter(
                referred_to=referred_counselor, user=referred_patient
            ).first()
            if referral:
                referral.referral_status = "Accepted"
                referral.save()

                # Send email to referred_by user
                subject = "Referral Accepted"
                message = f"Your referral for {referred_patient.first_name} {referred_patient.last_name} has been accepted."
                recipient_list = [referral.referred_by.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

                # Create notification for referred_by user
                Notification.objects.create(
                    notification_for=referral.referred_by,
                    notification=f"Your referral for {referred_patient.first_name} {referred_patient.last_name} has been accepted.",
                )

                return JsonResponse(
                    {"message": "Referral accepted and notification created."}
                )
            else:
                return JsonResponse(
                    {"error": "No referral found matching the criteria."},
                    status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return JsonResponse(
        {"error": "Only POST requests are allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@csrf_exempt
def reject_referral(request):
    if request.method == "POST":
        data = json.loads(request.body)
        referred_to_user_id = data.get("referredToUserId")
        patient_id = data.get("patientId")
        rejection_reason = data.get("reason")

        referred_counselor = get_object_or_404(CustomUser, id=referred_to_user_id)
        referred_patient = get_object_or_404(CustomUser, id=patient_id)

        try:
            referral = Referral.objects.get(
                referred_to=referred_counselor, user=referred_patient
            )
            if referral:
                referral.referral_status = "Rejected"
                referral.referral_remarks = rejection_reason
                referral.save()

                # Send email to referred_by user
                subject = "Referral Rejected"
                message = f"Your referral for {referred_patient.first_name} {referred_patient.last_name} has been rejected.\nReason: {rejection_reason}"
                recipient_list = [referral.referred_by.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

                # Create notification for referred_by user
                Notification.objects.create(
                    notification_for=referral.referred_by,
                    notification=f"Your referral for {referred_patient.first_name} {referred_patient.last_name} has been rejected. Reason: {rejection_reason}.",
                )

                return JsonResponse(
                    {"message": "Referral rejected and notification created."}
                )
            else:
                return JsonResponse(
                    {"error": "No referral found matching the criteria."},
                    status.HTTP_404_NOT_FOUND,
                )
        except Referral.DoesNotExist:
            return JsonResponse(
                {"error": "Referral does not exist."}, status.HTTP_404_NOT_FOUND
            )
    return JsonResponse(
        {"error": "Only POST requests are allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


def check_and_create_final_submission(user):
    rescreening = (
        Rescreening.objects.filter(user=user).order_by("-submission_date").first()
    )
    original_submission = (
        UserSubmission.objects.filter(user=user).order_by("-created_at").first()
    )

    if not original_submission:
        return None  # Early exit if no original submission is found

    final_submission_data = {
        "user": user,
        "initial_submission": original_submission,
        "submission_date": timezone.now(),
    }

    # Handle PHQ, GAD, and ACE Data (rescreening first, fallback to original)
    def update_data(field, rescreening, original_measurement):
        if rescreening and getattr(rescreening, f"{field}_data", None):
            final_submission_data.update(
                {
                    f"{field}_data": getattr(rescreening, f"{field}_data"),
                    f"{field}_score": getattr(rescreening, f"{field}_score"),
                    f"{field}_interpretation": getattr(
                        rescreening, f"{field}_interpretation"
                    ),
                }
            )
        elif original_measurement:
            final_submission_data.update(
                {
                    # Original submission doesn't store data as JSON
                    f"{field}_data": None,
                    f"{field}_score": getattr(
                        original_measurement, f"{field}_score", None
                    ),
                    f"{field}_interpretation": getattr(
                        original_measurement, f"{field}_measurement", None
                    ),
                }
            )

    original_measurement = Measurement.objects.filter(
        user_submission=original_submission
    ).first()

    for field in ["phq", "gad", "ace"]:
        update_data(field, rescreening, original_measurement)

    # Handle ASSIST data separately for rescreening or fallback to original submission
    if rescreening:
        assist_data = SubstanceRiskMeasurement.objects.filter(rescreening=rescreening)
        if assist_data.exists():
            assist_data_list = assist_data.values(
                "substance__name", "measurement", "risk_flag", "total_score"
            )
            final_submission_data["assist_data"] = list(assist_data_list)
        else:
            assist_sub = MeasurementAssist.objects.filter(
                user_submission=original_submission
            ).first()
            if assist_sub:
                final_submission_data["assist_data"] = {
                    "alcoholic_measurement": assist_sub.alcoholic_measurement,
                    "alcoholic_flag": assist_sub.alcoholic_flag,
                    "tobacco_measurement": assist_sub.tobacco_measurement,
                    "tobacco_flag": assist_sub.tobacco_flag,
                    "cannabis_measurement": assist_sub.cannabis_measurement,
                    "cannabis_flag": assist_sub.cannabis_flag,
                    "cocaine_measurement": assist_sub.cocaine_measurement,
                    "cocaine_flag": assist_sub.cocaine_flag,
                    "amphetamine_measurement": assist_sub.amphetamine_measurement,
                    "amphetamine_flag": assist_sub.amphetamine_flag,
                    "inhalants_measurement": assist_sub.inhalants_measurement,
                    "inhalants_flag": assist_sub.inhalants_flag,
                    "sedatives_measurement": assist_sub.sedatives_measurement,
                    "sedatives_flag": assist_sub.sedatives_flag,
                    "hallucinogens_measurement": assist_sub.hallucinogens_measurement,
                    "hallucinogens_flag": assist_sub.hallucinogens_flag,
                    "opioids_measurement": assist_sub.opioids_measurement,
                    "opioids_flag": assist_sub.opioids_flag,
                    "injection_measurement": assist_sub.injection_measurement,
                    "injection_flag": assist_sub.injection_flag,
                    "other_measurement": assist_sub.other_measurement,
                    "other_flag": assist_sub.other_flag,
                    "other_name": assist_sub.other_name,
                }

    final_submission, created = FinalUserSubmission.objects.update_or_create(
        user=user,
        initial_submission=original_submission,
        defaults=final_submission_data,
    )

    return final_submission


@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def list_final_submissions(request):
    users_with_rescreenings = CustomUser.objects.filter(
        rescreenings__isnull=False
    ).distinct()

    for user in users_with_rescreenings:
        check_and_create_final_submission(user)

    final_submissions = FinalUserSubmission.objects.all().order_by("-submission_date")
    serializer = FinalUserSubmissionSerializer(final_submissions, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def retrieve_final_submission(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    check_and_create_final_submission(user)

    final_submissions = FinalUserSubmission.objects.filter(user=user).order_by(
        "-submission_date"
    )
    serializer = FinalUserSubmissionSerializer(final_submissions, many=True)
    return Response(serializer.data)


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Referral.objects.all()
        user = self.request.query_params.get("user", None)
        referred_by = self.request.query_params.get("referred_by", None)

        if user is not None:
            queryset = queryset.filter(user=user)
        if referred_by is not None:
            queryset = queryset.filter(referred_by=referred_by)

        return queryset

    @action(detail=False, methods=["get"], url_path="by-status")
    def filter_by_status(self, request):
        status = request.query_params.get("status", None)
        if status is not None:
            referrals = self.get_queryset().filter(referral_status=status)
            serializer = self.get_serializer(referrals, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "Status parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="referred-to")
    def referred_to_details(self, request, pk=None):
        referral = self.get_object()
        referred_to_user = referral.referred_to
        if referred_to_user:
            user_serializer = CustomUserSerializer(referred_to_user)
            return Response(user_serializer.data)
        return Response(
            {"detail": "No referred_to user found for this referral."},
            status.HTTP_404_NOT_FOUND,
        )


def create_service_and_treatments(request):
    try:
        with transaction.atomic():
            service_and_treatment_object_list = []
            case_based_submissions = CaseBasedSubmission.objects.only("id", "user")
            event_based_submissions = EventBasedSubmission.objects.only("id", "user")
            final_user_submissions = FinalUserSubmission.objects.only("id", "user")
            gyalsung_profiles = GyalsungUserProfile.objects.only("id")

            case_content_type = ContentType.objects.get_for_model(CaseBasedSubmission)
            event_content_type = ContentType.objects.get_for_model(EventBasedSubmission)
            final_content_type = ContentType.objects.get_for_model(FinalUserSubmission)
            gyalsung_content_type = ContentType.objects.get_for_model(
                GyalsungUserProfile
            )

            for case_submission in case_based_submissions:
                if not ServiceAndTreatment.objects.filter(
                    content_type=case_content_type, object_id=case_submission.id
                ).exists():
                    service_and_treatment_object_list.append(
                        ServiceAndTreatment(
                            content_type=case_content_type,
                            object_id=case_submission.id,
                            user=case_submission.user,
                            date=timezone.now(),
                            assessment_status="Not Conducted",
                            case_status="On Going",
                            counseling="Waiting List",
                            updated_by=None,
                        )
                    )

            for event_submission in event_based_submissions:
                if not ServiceAndTreatment.objects.filter(
                    content_type=event_content_type, object_id=event_submission.id
                ).exists():
                    service_and_treatment_object_list.append(
                        ServiceAndTreatment(
                            content_type=event_content_type,
                            object_id=event_submission.id,
                            user=event_submission.user,
                            date=timezone.now(),
                            assessment_status="Not Conducted",
                            case_status="On Going",
                            counseling="Waiting List",
                            updated_by=None,
                        )
                    )

            for final_submission in final_user_submissions:
                if not ServiceAndTreatment.objects.filter(
                    content_type=final_content_type, object_id=final_submission.id
                ).exists():
                    service_and_treatment_object_list.append(
                        ServiceAndTreatment(
                            content_type=final_content_type,
                            object_id=final_submission.id,
                            user=final_submission.user,
                            date=timezone.now(),
                            assessment_status="Not Conducted",
                            case_status="On Going",
                            counseling="Waiting List",
                            updated_by=None,
                        )
                    )

            for gyalsung_profile in gyalsung_profiles:
                if not ServiceAndTreatment.objects.filter(
                    content_type=gyalsung_content_type, object_id=gyalsung_profile.id
                ).exists():
                    service_and_treatment_object_list.append(
                        ServiceAndTreatment(
                            content_type=gyalsung_content_type,
                            object_id=gyalsung_profile.id,
                            user=None,  # No user field for GyalsungUserProfile
                            date=timezone.now(),
                            assessment_status="Not Conducted",
                            case_status="On Going",
                            counseling="Waiting List",
                            updated_by=None,
                        )
                    )

            # creating all the service and treatment records in a single db query
            print(
                ">>>> len service_and_treatment_object_list:",
                len(service_and_treatment_object_list),
            )
            ServiceAndTreatment.objects.bulk_create(service_and_treatment_object_list)

        return JsonResponse(
            {
                "status": "success",
                "message": "Service and Treatment records created successfully.",
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def get_notifications(request, user_id):
    if request.method == "GET":
        try:
            notifications = Notification.objects.filter(
                notification_for__id=user_id
            ).values("id", "notification", "notification_status", "created_at")

            return JsonResponse(
                {"notifications": list(notifications)}, status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse(
            {"error": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@csrf_exempt
def mark_notification_as_read(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            notification_id = data.get("notification_id")

            if not notification_id:
                return JsonResponse(
                    {"error": "Notification ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            notification = get_object_or_404(Notification, id=notification_id)
            notification.mark_as_read()

            return JsonResponse(
                {"message": "Notification marked as read"}, status.HTTP_200_OK
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return JsonResponse(
            {"error": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
