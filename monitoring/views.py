from datetime import date
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from measurement.models import Measurement, MeasurementAssist, Submission, UserSubmission
from django.views.decorators.csrf import csrf_exempt
from access.models import Agency, CustomUser, UserAgency
from monitoring.serializers import FinalUserSubmissionSerializer
from screening.models import CaseBasedSubmission, CaseScreening, EventBasedSubmission, EventScreening
from .models import FinalUserSubmission, Rescreening, ServiceAndTreatment, Referral, ServiceAndTreatmentHistory, Substance, SubstanceRiskMeasurement
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.http import require_GET
from django.forms.models import model_to_dict
from django.db import transaction
from datetime import date
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def submit_rescreening(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        rescreened_by_id = request.POST.get('rescreened_by')  # Retrieve rescreened_by from the request

        user = get_object_or_404(CustomUser, id=user_id)
        rescreened_by_user = get_object_or_404(CustomUser, id=rescreened_by_id)  # Fetch the rescreened_by user

        age = calculate_age(user.date_of_birth)

        assist_data_json = request.POST.get('assistRiskSeverity', '{}')
        assist_data = json.loads(assist_data_json) if assist_data_json else {}

        # Extract interpretation data from the incoming request
        gad_data_json = request.POST.get('gadData', '{}')
        gad_data = json.loads(gad_data_json) if gad_data_json else {}
        gad_score = gad_data.get('totalScore', 0)
        gad_interpretation = gad_data.get('interpretation', '')

        phq_data_json = request.POST.get('phqData', '{}')
        phq_data = json.loads(phq_data_json) if phq_data_json else {}
        phq_score = phq_data.get('totalScore', 0)
        phq_interpretation = phq_data.get('interpretation', '')

        ace_data_json = request.POST.get('aceData', '{}')
        ace_data = json.loads(ace_data_json) if ace_data_json else {}
        ace_score = ace_data.get('totalScore', 0)
        ace_interpretation = ace_data.get('interpretation', '')

        with transaction.atomic():
            rescreening, created = Rescreening.objects.update_or_create(
                user=user,
                defaults={
                    'gad_data': gad_data_json,
                    'gad_score': gad_score,
                    'gad_interpretation': gad_interpretation,  # Save GAD interpretation
                    'phq_data': phq_data_json,
                    'phq_score': phq_score,
                    'phq_interpretation': phq_interpretation,  # Save PHQ interpretation
                    'ace_data': ace_data_json,
                    'ace_score': ace_score,
                    'ace_interpretation': ace_interpretation,  # Save ACE interpretation
                    'school_env_data': request.POST.get('schoolEnvData', '{}'),
                    'rescreened': True,
                    'screened_by': rescreened_by_user,  # Save the rescreened_by user
                    'rescreening_date': timezone.now()  # Save the current date/time for rescreening
                }
            )

            # Save substance risk measurements
            for substance, risk_level in assist_data.items():
                total_score_str = risk_level.split()[1]
                total_score = float(total_score_str.strip('()'))
                risk_flag = risk_level.split()[0]

                # Create or update substance risk measurement
                substance_instance, _ = Substance.objects.get_or_create(name=substance)
                SubstanceRiskMeasurement.objects.create(
                    substance=substance_instance,
                    rescreening=rescreening,
                    measurement=total_score,
                    risk_flag=risk_flag
                )

            # Set the rescreened field of the associated UserSubmission to True
            user_submission = UserSubmission.objects.get(user=user)
            user_submission.rescreened = True
            user_submission.save()

        # Return appropriate message depending on whether the rescreening was created or updated
        message = 'Rescreening data saved successfully.' if created else 'Rescreening data updated successfully.'

        return JsonResponse({'message': message})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})


def get_non_green_flags(request):
    rescreening_list = []

    # Iterate over all UserSubmission instances
    for submission in UserSubmission.objects.filter(rescreened=False, mark_as_safe=False):
        # Initialize a dictionary to store data for the current submission
        submission_data = {
            'submission_id': submission.id,
            'flags': {},  # Initialize flags dictionary
            'user_details': {},
            'measurement_data': {},
            'measurement_assist_data': {},
            'user_agency_data': {},
            'diagnosis': ''  # Initialize diagnosis field
        }

        # Fetch Measurement and MeasurementAssist instances for the current submission
        measurement = Measurement.objects.filter(
            user_submission=submission).first()
        measurement_assist = MeasurementAssist.objects.filter(
            user_submission=submission).first()

        # Fetch Submission details for the submission
        submission_details = Submission.objects.filter(
            user_submission=submission).first()
        if submission_details:
            submission_data['diagnosis'] = submission_details.diagnosis
            submission_data['created_at'] = submission_details.created_at

        # Fetch user details for the submission
        middle_name = submission.user.middle_name if submission.user.middle_name else ''
        full_name = f"{submission.user.first_name} {middle_name} {submission.user.last_name}".strip()
        user_details = {
            'full_name': full_name,
            'age': calculate_age(submission.user.date_of_birth),
            'sex': submission.user.gender,
            'user_id': submission.user.id
        }
        submission_data['user_details'] = user_details

        # Fetch user agency details for the submission
        if submission.user.active_agency:
            user_agency_data = {}
            try:
                user_agency = submission.user.agency_details  # Accessing the UserAgency object
                user_agency_data = {
                    'agency_name': user_agency.agency.agency_name,
                    'user_role_agency': user_agency.user_role_agency,
                    'user_class': user_agency.user_class,
                    'user_stream': user_agency.user_stream,
                    'user_sub_class': user_agency.user_sub_class,
                    'user_dzongkhag': submission.user.active_agency.present_dzongkhag,
                }
            except UserAgency.DoesNotExist:
                # Handle the case where UserAgency object does not exist for the CustomUser
                user_agency_data = {}  # Set user_agency_data to empty dictionary or handle as needed
            submission_data['user_agency_data'] = user_agency_data

        # Check MeasurementAssist flags
        if measurement_assist:
            # Iterate over each field in MeasurementAssist
            for field in measurement_assist._meta.fields:
                # Check if the field represents a flag
                if field.name.endswith('_flag'):
                    flag_value = getattr(measurement_assist, field.name)
                    # If the flag is not green, add it to flags dictionary
                    if flag_value != 'green':
                        submission_data['flags'][field.name] = flag_value

        # Check Measurement flags
        if measurement:
            # Iterate over each field in Measurement
            for field in measurement._meta.fields:
                # Check if the field represents a flag
                if field.name.endswith('_flag'):
                    flag_value = getattr(measurement, field.name)
                    # If the flag is not green, add it to flags dictionary
                    if flag_value != 'green':
                        submission_data['flags'][field.name] = flag_value

        # If there are non-green flags, add the submission data to the rescreening list
        if submission_data['flags']:
            # Add measurement data if available
            if measurement:
                submission_data['measurement_data'] = model_to_dict(
                    measurement)
            # Add measurement assist data if available
            if measurement_assist:
                submission_data['measurement_assist_data'] = model_to_dict(
                    measurement_assist)
            rescreening_list.append(submission_data)

    return {'Rescreening List': rescreening_list}


@csrf_exempt
def process_rescreening(request):
    # Retrieve saved records from Rescreening table
    rescreening_records = get_non_green_flags(request)

    # Log the data being returned
    logger.debug("Response data:")
    logger.debug(rescreening_records)

    # Convert the dictionary to JSON and return it as JsonResponse
    return JsonResponse(rescreening_records)


def calculate_age(born):
    today = date.today()
    age = today.year - born.year - \
        ((today.month, today.day) < (born.month, born.day))
    return age


def get_user_details(user):
    user_agency = UserAgency.objects.filter(user=user).first()
    agency_details = None
    if user_agency:
        agency_details = {
            'agency_name': user_agency.agency.agency_name,
            'agency_code': user_agency.agency.agency_code,
            'parent_occupation': user_agency.parent_occupation,
            'parent_status': user_agency.parent_status,

        }
    return {
        'id': user.id,
        'full_name': f"{user.first_name} {user.middle_name or ''} {user.last_name}",
        'age': (timezone.now().date() - user.date_of_birth).days // 365,
        'gender': user.gender,
        'user_agency': agency_details,
    }


def generateServiceAndTreatment(request):
    try:
        rescreenings = Rescreening.objects.all()

        # Collect existing service and treatments to avoid duplicates
        existing_service_and_treatments = ServiceAndTreatment.objects.filter(
            user__in=[res.user for res in rescreenings],
            date__in=[res.submission_date.date()
                      for res in rescreenings if res.submission_date]
        ).values_list('user', 'date')

        # Collecting newly created ServiceAndTreatment records
        new_service_and_treatments = []
        for rescreening in rescreenings:
            if rescreening.submission_date and (rescreening.user, rescreening.submission_date.date()) not in existing_service_and_treatments:
                new_service_and_treatments.append(ServiceAndTreatment(
                    user=rescreening.user,
                    date=rescreening.submission_date.date(),
                    assessment_status='Not Conducted',
                    case_status='On Going',
                    counseling='Waiting List',
                    follow_up='',
                    comments=''
                ))
                rescreening.rescreened = True

        ServiceAndTreatment.objects.bulk_create(new_service_and_treatments)
        Rescreening.objects.bulk_update(rescreenings, ['rescreened'])

        # Collecting data for CaseScreening and CaseBasedSubmission
        case_screenings = CaseScreening.objects.all()
        case_based_submissions = CaseBasedSubmission.objects.filter(
            case__in=case_screenings
        )

        # Collecting data for EventScreening and EventBasedSubmission
        event_screenings = EventScreening.objects.all()
        event_based_submissions = EventBasedSubmission.objects.filter(
            event__in=event_screenings
        )

        # Formatting ServiceAndTreatment data for the response
        service_and_treatments_data = [
            {
                'user': get_user_details(obj.user),
                'date': obj.date,
                'assessment_status': obj.assessment_status,
                'case_status': obj.case_status,
                'counseling': obj.counseling,
                'follow_up': obj.follow_up,
                'comments': obj.comments,
            }
            for obj in ServiceAndTreatment.objects.all()
        ]

        # Formatting CaseScreening and CaseBasedSubmission data
        case_screening_data = [
            {
                'user': get_user_details(case.user),
                'case_name': case.case_name,
                'purpose': case.purpose,
                'date': case.date,
                'dzongkhag': case.dzongkhag,
                'counselor': case.counselor,
            }
            for case in case_screenings
        ]

        case_based_submission_data = [
            {
                'user': get_user_details(sub.user),
                'case_name': sub.case.case_name,
                'gad_score': sub.gad_score,
                'phq_score': sub.phq_score,
                'ace_score': sub.ace_score,
            }
            for sub in case_based_submissions
        ]

        # Formatting EventScreening and EventBasedSubmission data
        event_screening_data = [
            {
                'event_name': event.event_name,
                'location': event.location,
                'counselor': event.counselor,
                'start_date': event.start_date,
                'end_date': event.end_date,
            }
            for event in event_screenings
        ]

        event_based_submission_data = [
            {
                'user': get_user_details(sub.user),
                'event_name': sub.event.event_name,
                'gad_score': sub.gad_score,
                'phq_score': sub.phq_score,
                'ace_score': sub.ace_score,
            }
            for sub in event_based_submissions
        ]

        # Fetching counselor data (optimized)
        counselors = CustomUser.objects.exclude(
            Q(role__in=['student', 'public']) | Q(role__contains='_admin')
        ).values('first_name', 'middle_name', 'last_name', 'active_agency__agency_name', 'role')

        # Returning combined JSON response
        return JsonResponse({
            'message': 'ServiceAndTreatment, CaseScreening, and EventScreening records updated successfully',
            'service_and_treatments_data': service_and_treatments_data,
            'case_screening_data': case_screening_data,
            'case_based_submission_data': case_based_submission_data,
            'event_screening_data': event_screening_data,
            'event_based_submission_data': event_based_submission_data,
            'counselors': list(counselors)
        }, status=200)

    except Exception as e:
        logger.error(f"Error in generateServiceAndTreatment: {e}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


@csrf_exempt
@require_POST
def update_service_and_treatment(request):
    if request.method == 'POST':
        try:
            logger.info(
                'Received POST request to update service and treatment')

            # Get the update data from the request body
            data = json.loads(request.body)
            update_data = data.get('updateData')

            custom_user_id = update_data.get('id')
            service_and_treatments = ServiceAndTreatment.objects.filter(
                user_id=custom_user_id)

            # Check if any ServiceAndTreatment instance is found
            if not service_and_treatments.exists():
                error_msg = 'ServiceAndTreatment not found for user_id: {}'.format(
                    custom_user_id)
                return JsonResponse({'error': error_msg}, status=404)

            # Get the counselor's CustomUser instance
            counselor_id = update_data.get('updated_by')
            counselor = get_user_model().objects.get(id=counselor_id)

            for service_and_treatment in service_and_treatments:
                # Create a ServiceAndTreatmentHistory instance to store the changes
                history_entry = ServiceAndTreatmentHistory.objects.create(
                    service_and_treatment=service_and_treatment,
                    updated_by=counselor,
                    updated_at=timezone.now(),
                    # Assuming you want to store all changes as JSON
                    changes=json.dumps(update_data)
                )
                history_entry.save()

                # Update the ServiceAndTreatment instance with the latest data
                service_and_treatment.assessment_status = update_data.get(
                    'assessment_status')
                service_and_treatment.case_status = update_data.get(
                    'case_status')
                service_and_treatment.counseling = update_data.get(
                    'counseling')
                service_and_treatment.follow_up = update_data.get('follow_up')
                service_and_treatment.comments = update_data.get('comments')
                service_and_treatment.updated_by = counselor

                service_and_treatment.save()

            # Return success response
            return JsonResponse({'message': 'ServiceAndTreatment updated successfully'}, status=200)
        except Exception as e:
            error_msg = f'An error occurred: {str(e)}'
            return JsonResponse({'error': error_msg}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def getReferralList(request):
    referrals = Referral.objects.all().select_related('user', 'referred_by', 'referred_to').prefetch_related(
        Prefetch('service_and_treatment',
                 queryset=ServiceAndTreatment.objects.select_related('user'))
    )

    referral_list = []

    for referral in referrals:
        birth_date = referral.user.date_of_birth
        age = calculate_age(birth_date)

        user_data = {
            'date_of_birth': birth_date.strftime('%Y-%m-%d'),
            'name': f"{referral.user.first_name} {referral.user.middle_name} {referral.user.last_name}",
            'age': age,
            'gender': referral.user.gender,
            'patient_id': referral.user.id
        }

        referral_data = {
            'user_data': user_data,
            'referred_by': {
                'username': referral.referred_by.username if referral.referred_by else None
            },
            'referred_to': {
                'name': referral.referred_to_name,
                'user_id': referral.referred_to_id
            },
            'date': referral.date,
            'referral_status': referral.referral_status,
            'referral_remarks': referral.referral_remarks,
            # Include details from ServiceAndTreatment model
            'assessment_status': referral.service_and_treatment.assessment_status if referral.service_and_treatment else None,
            'counseling_status': referral.service_and_treatment.counseling if referral.service_and_treatment else None,
            'follow_up': referral.service_and_treatment.follow_up if referral.service_and_treatment else None,
            'comments': referral.service_and_treatment.comments if referral.service_and_treatment else None,
        }
        referral_list.append(referral_data)

    return JsonResponse({'referral_list': referral_list}, status=200)


@csrf_exempt
def update_referral_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        refer_data = data.get('referData')

        if refer_data:
            referred_by_id = refer_data.get('referred_by')
            referred_to_id = refer_data.get('referred_to_name')
            user_id = refer_data.get('user')

            if not all([referred_by_id, referred_to_id, user_id]):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                referred_by = CustomUser.objects.get(id=referred_by_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Referred by user does not exist'}, status=400)

            try:
                referred_to = CustomUser.objects.get(id=referred_to_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Referred to user does not exist'}, status=400)

            referral_status = 'Awaiting'
            referral, created = Referral.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'referred_by': referred_by,
                    'referred_to': referred_to,
                    'referred_to_name': referred_to.first_name + ' ' + referred_to.last_name,
                    'referral_status': referral_status,
                    'date': timezone.now(),
                }
            )

            # Update the referred field in ServiceAndTreatment model based on referral status
            with transaction.atomic():
                service_and_treatment = ServiceAndTreatment.objects.filter(
                    user=user_id).first()
                if service_and_treatment:
                    if referral.referral_status:
                        service_and_treatment.referred = 'Referred'
                        pass
                    service_and_treatment.save()

            return JsonResponse({'message': 'Referral saved successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Data not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# function for getting users details:
def get_user_monitoring_details(request):
    user_id = request.GET.get('user_id')

    if user_id is None:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    user = get_object_or_404(CustomUser, pk=user_id)

    try:
        user_agency = UserAgency.objects.get(user=user)
        agency_details = {
            'agency_name': user_agency.agency.agency_name,
            'agency_code': user_agency.agency.agency_code,
            'agency_parent': user_agency.agency.agency_parent,
            'parent_occupation': user_agency.parent_occupation,
            'parent_status': user_agency.parent_status,
        }
    except UserAgency.DoesNotExist:
        agency_details = None

    agency_active_details = []
    if user.active_agency:
        agency_active_details.append({
            'present_dzongkhag': user.active_agency.present_dzongkhag,
            'present_gewog': user.active_agency.present_gewog,
            'present_village': user.active_agency.present_village,
        })

    service_and_treatment_details = list(
        ServiceAndTreatment.objects.filter(user=user).values())

    referral_details = list(Referral.objects.filter(user=user).values())

    user_submissions = UserSubmission.objects.filter(user=user)
    diagnosis_details = list(
        Submission.objects.filter(user_submission__in=user_submissions).values('diagnosis'))

    rescreenings = Rescreening.objects.filter(user=user)
    rescreening_details = []
    for rescreening in rescreenings:
        rescreening_data = {
            'id': rescreening.id,
            'submission_date': rescreening.submission_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        rescreening_details.append(rescreening_data)

    substance_risk_measurements = SubstanceRiskMeasurement.objects.filter(
        rescreening__in=rescreenings)
    substance_risk_measurement_details = []
    for measurement in substance_risk_measurements:
        substance_name = measurement.substance.name
        measurement_data = {
            'id': measurement.id,
            'substance_name': substance_name,
            'measurement': measurement.measurement,
            'risk_flag': measurement.risk_flag,
            'total_score': measurement.total_score,
        }
        substance_risk_measurement_details.append(measurement_data)

    user_details = {
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'identity_number': user.identity_number,
        'nationality': user.nationality,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
        'gender': user.gender,
        'email': user.email,
        'mob_number': user.mob_number,
        'father_name': user.father_name,
        'mother_name': user.mother_name,
        'perm_add_village': user.perm_add_village,
        'perm_add_gewog': user.perm_add_gewog,
        'perm_add_dzongkhag': user.perm_add_dzongkhag,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
        'active_agency': user.active_agency.agency_name if user.active_agency else None,
        'ps_add_village': user.ps_add_village,
        'ps_add_gewog': user.ps_add_gewog,
        'ps_add_dzongkhag': user.ps_add_dzongkhag,
        'is_gyalsung': user.is_gyalsung,
        'academy_code': user.academy_code,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'role': user.role,
        'access_level': user.access_level,
        'agency_details': agency_details,
        'service_and_treatment_details': service_and_treatment_details,
        'referral_details': referral_details,
        'rescreening_details': rescreening_details,
        'substance_risk_measurement_details': substance_risk_measurement_details,
        'agency': agency_active_details,
        'diagnosis_details': diagnosis_details
    }

    return JsonResponse(user_details)


@csrf_exempt
def accept_referral(request):
    logger.info("Accept referral endpoint called.")

    if request.method == 'POST':
        logger.debug("Request method is POST.")

        data = json.loads(request.body)
        referred_to_user_id = data.get('referredToUserId')
        patient_id = data.get('patientId')

        logger.debug(
            f"referredToUserId: {referred_to_user_id}, patientId: {patient_id}")

        # Get the referred counselor and patient
        referred_counselor = get_object_or_404(
            CustomUser, id=referred_to_user_id)
        referred_patient = get_object_or_404(CustomUser, id=patient_id)

        logger.debug(
            f"Referred counselor: {referred_counselor}, Referred patient: {referred_patient}")

        try:
            # Check if a referral exists
            referral = Referral.objects.filter(
                referred_to=referred_counselor, user=referred_patient).first()

            logger.debug(f"Referral query result: {referral}")

            if referral:
                # Update referral status to 'Accepted'
                referral.referral_status = 'Accepted'
                referral.save()
                logger.info("Referral status updated to 'Accepted'.")
                return JsonResponse({'message': 'Referral accepted successfully.'})
            else:
                logger.error("No referral found matching the criteria.")
                return JsonResponse({'error': 'No referral found matching the criteria.'}, status=404)
        except Exception as e:
            logger.exception("An error occurred while accepting the referral.")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        logger.error("Invalid request method.")
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def reject_referral(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        referred_to_user_id = data.get('referredToUserId')
        patient_id = data.get('patientId')
        rejection_reason = data.get('reason')

        # Get the referred counselor and patient
        referred_counselor = get_object_or_404(
            CustomUser, id=referred_to_user_id)
        referred_patient = get_object_or_404(CustomUser, id=patient_id)

        try:
            referral = Referral.objects.get(
                referred_to=referred_counselor, user=referred_patient)

            if referral:
                referral.referral_status = 'Rejected'
                referral.referral_remarks = rejection_reason
                referral.save()
                return JsonResponse({'message': 'Referral rejected successfully.'})
            else:
                return JsonResponse({'error': 'No referral found matching the criteria.'}, status=404)
        except Referral.DoesNotExist:
            return JsonResponse({'error': 'Referral does not exist.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def check_and_create_final_submission(user):
    rescreening = Rescreening.objects.filter(user=user).order_by('-submission_date').first()
    original_submission = UserSubmission.objects.filter(user=user).order_by('-created_at').first()

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
            final_submission_data.update({
                f'{field}_data': getattr(rescreening, f'{field}_data'),
                f'{field}_score': getattr(rescreening, f'{field}_score'),
                f'{field}_interpretation': getattr(rescreening, f'{field}_interpretation'),
            })
        elif original_measurement:
            final_submission_data.update({
                f'{field}_data': None,  # Original submission doesn't store data as JSON
                f'{field}_score': getattr(original_measurement, f'{field}_score', None),
                f'{field}_interpretation': getattr(original_measurement, f'{field}_measurement', None),
            })

    original_measurement = Measurement.objects.filter(user_submission=original_submission).first()

    for field in ['phq', 'gad', 'ace']:
        update_data(field, rescreening, original_measurement)

    # Handle ASSIST data separately for rescreening or fallback to original submission
    if rescreening:
        assist_data = SubstanceRiskMeasurement.objects.filter(rescreening=rescreening)
        if assist_data.exists():
            assist_data_list = assist_data.values('substance__name', 'measurement', 'risk_flag', 'total_score')
            final_submission_data['assist_data'] = list(assist_data_list)
        else:
            assist_sub = MeasurementAssist.objects.filter(user_submission=original_submission).first()
            if assist_sub:
                final_submission_data['assist_data'] = {
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
@api_view(['GET'])
@permission_classes([AllowAny])
def list_final_submissions(request):
    users_with_rescreenings = CustomUser.objects.filter(rescreenings__isnull=False).distinct()

    for user in users_with_rescreenings:
        check_and_create_final_submission(user)

    final_submissions = FinalUserSubmission.objects.all().order_by('-submission_date')
    serializer = FinalUserSubmissionSerializer(final_submissions, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def retrieve_final_submission(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    check_and_create_final_submission(user)

    final_submissions = FinalUserSubmission.objects.filter(user=user).order_by('-submission_date')
    serializer = FinalUserSubmissionSerializer(final_submissions, many=True)
    return Response(serializer.data)
