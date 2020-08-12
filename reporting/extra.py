import logging
from datetime import date, datetime

from django.contrib.auth.models import User as Token
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from access.models import CustomUser, UserAgency
from measurement.models import Measurement
from monitoring.models import Rescreening, ServiceAndTreatment, SubstanceRiskMeasurement

# i am not getting why the UserArchive is that some deprecated model
from reporting.models import Reporting, UserArchive

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@csrf_exempt
def update_user_archive(request):
    excluded_roles = [
        CustomUser.ROLE_CLINICAL_COUNSELOR,
        CustomUser.ROLE_GYALSUNG_COUNSELOR,
        CustomUser.ROLE_SCHOOL_COUNSELOR,
        CustomUser.ROLE_TRAINED_PROFESSIONAL,
        CustomUser.ROLE_ADMIN,
        CustomUser.ROLE_RD_ADMIN,
        CustomUser.ROLE_SUD_ADMIN,
        CustomUser.ROLE_AAA_ADMIN,
    ]

    users_to_process = CustomUser.objects.exclude(role__in=excluded_roles)

    for user in users_to_process:
        user_agency = UserAgency.objects.filter(user=user).first()
        user_submission = user.usersubmission_set.first()
        service_and_treatment = ServiceAndTreatment.objects.filter(user=user).first()
        rescreenings_to_process = Rescreening.objects.all()

        # Check if a UserArchive instance with the same identity_number exists
        existing_user_archive = UserArchive.objects.filter(
            identity_number=user.identity_number
        ).first()

        if user_agency:
            agency = user_agency.agency
            user_data = {
                "identity_number": user.identity_number,
                "nationality": user.nationality,
                "first_name": user.first_name,
                "middle_name": user.middle_name,
                "last_name": user.last_name,
                "date_of_birth": user.date_of_birth,
                "gender": user.gender,
                "mobile_number": user.mob_number,
                "is_gyalsung": user.is_gyalsung,
                "academy_code": user.academy_code,
                "role": user.role,
                "user_code": user_agency.user_code,
                "parent_status": user_agency.parent_status,
                "current_living_with": user_agency.current_living_with,
                "user_role_agency": user_agency.user_role_agency,
                "user_class": user_agency.user_class,
                "user_stream": user_agency.user_stream,
                "user_sub_class": user_agency.user_sub_class,
                "agency_code": agency.agency_code,
                "agency_name": agency.agency_name,
                "agency_parent": agency.agency_parent,
                "present_dzongkhag": agency.present_dzongkhag,
                "present_gewog": agency.present_gewog,
                "present_village": agency.present_village,
                "ps_add_village": user.ps_add_village,
                "ps_add_gewog": user.ps_add_gewog,
                "ps_add_dzongkhag": user.ps_add_dzongkhag,
            }

            if existing_user_archive:
                # Update existing UserArchive instance
                for field, value in user_data.items():
                    setattr(existing_user_archive, field, value)
                existing_user_archive.save()
            else:
                # Create new UserArchive instance
                user_archive = UserArchive(**user_data)
                user_archive.save()
        else:
            pass

        if user_submission:
            measurement = Measurement.objects.filter(
                user=user, user_submission=user_submission
            ).first()

            if measurement:
                user_data = {
                    # Populate substance use information
                    "gad_measurement": measurement.gad_measurement,
                    "gad_flag": measurement.gad_flag,
                    "phq_measurement": measurement.phq_measurement,
                    "phq_flag": measurement.phq_flag,
                    "suicidal_measurement": measurement.suicidal_measurement,
                    "suicidal_flag": measurement.suicidal_flag,
                    "ace_measurement": measurement.ace_measurement,
                    "ace_flag": measurement.ace_flag,
                    "overall_flag": measurement.overall_flag,
                    "alcoholic_measurement": (
                        measurement.assist.alcoholic_measurement
                        if measurement.assist
                        else None
                    ),
                    "alcoholic_flag": (
                        measurement.assist.alcoholic_flag
                        if measurement.assist
                        else None
                    ),
                    "tobacco_measurement": (
                        measurement.assist.tobacco_measurement
                        if measurement.assist
                        else None
                    ),
                    "tobacco_flag": (
                        measurement.assist.tobacco_flag if measurement.assist else None
                    ),
                    "cannabis_measurement": (
                        measurement.assist.cannabis_measurement
                        if measurement.assist
                        else None
                    ),
                    "cannabis_flag": (
                        measurement.assist.cannabis_flag if measurement.assist else None
                    ),
                    "cocaine_measurement": (
                        measurement.assist.cocaine_measurement
                        if measurement.assist
                        else None
                    ),
                    "cocaine_flag": (
                        measurement.assist.cocaine_flag if measurement.assist else None
                    ),
                    "amphetamine_measurement": (
                        measurement.assist.amphetamine_measurement
                        if measurement.assist
                        else None
                    ),
                    "amphetamine_flag": (
                        measurement.assist.amphetamine_flag
                        if measurement.assist
                        else None
                    ),
                    "inhalants_measurement": (
                        measurement.assist.inhalants_measurement
                        if measurement.assist
                        else None
                    ),
                    "inhalants_flag": (
                        measurement.assist.inhalants_flag
                        if measurement.assist
                        else None
                    ),
                    "sedatives_measurement": (
                        measurement.assist.sedatives_measurement
                        if measurement.assist
                        else None
                    ),
                    "sedatives_flag": (
                        measurement.assist.sedatives_flag
                        if measurement.assist
                        else None
                    ),
                    "hallucinogens_measurement": (
                        measurement.assist.hallucinogens_measurement
                        if measurement.assist
                        else None
                    ),
                    "hallucinogens_flag": (
                        measurement.assist.hallucinogens_flag
                        if measurement.assist
                        else None
                    ),
                    "opioids_measurement": (
                        measurement.assist.opioids_measurement
                        if measurement.assist
                        else None
                    ),
                    "opioids_flag": (
                        measurement.assist.opioids_flag if measurement.assist else None
                    ),
                    "injection_measurement": (
                        measurement.assist.injection_measurement
                        if measurement.assist
                        else None
                    ),
                    "injection_flag": (
                        measurement.assist.injection_flag
                        if measurement.assist
                        else None
                    ),
                    "other_measurement": (
                        measurement.assist.other_measurement
                        if measurement.assist
                        else None
                    ),
                    "other_flag": (
                        measurement.assist.other_flag if measurement.assist else None
                    ),
                    "other_name": (
                        measurement.assist.other_name if measurement.assist else None
                    ),
                    # Submission Details
                    "test_type": user_submission.test_type.name,
                    "rescreened": user_submission.rescreened,
                    "created_at": user_submission.created_at,
                }

                # Save data to UserArchive
                user_archive = UserArchive(**user_data)
                user_archive.save()
            else:
                # Handle cases where measurement data is not found
                pass

            if service_and_treatment:
                service_and_treatment_data = {
                    "assessment_status": service_and_treatment.assessment_status,
                    "case_status": service_and_treatment.case_status,
                    "counseling": service_and_treatment.counseling,
                    "follow_up": service_and_treatment.follow_up,
                    "comments": service_and_treatment.comments,
                    "updated_at": service_and_treatment.updated_at,
                    "referred": service_and_treatment.referred,
                }

                for field, value in service_and_treatment_data.items():
                    setattr(service_and_treatment, field, value)
                service_and_treatment.save()

            referral_instance = service_and_treatment.referral
            if referral_instance:
                referral_data = {
                    "referred_by": referral_instance.referred_by,
                    "date": referral_instance.date,
                    "referred_to": referral_instance.referred_to,
                    "referred_to_name": referral_instance.referred_to_name,
                    "referral_status": referral_instance.referral_status,
                    "referral_remarks": referral_instance.referral_remarks,
                }

                # Update Referral Details
                for field, value in referral_data.items():
                    setattr(referral_instance, field, value)
                referral_instance.save()

            else:
                # Handle cases where ServiceAndTreatment instance is not found
                pass

        for rescreening in rescreenings_to_process:

            interpretations = {}
            scores = {}

            risk_measurements = SubstanceRiskMeasurement.objects.filter(
                rescreening=rescreening
            )

            # Loop through the risk measurements to populate interpretations and scores
            for measurement in risk_measurements:
                substance_name = measurement.substance.name
                interpretations[substance_name] = measurement.risk_flag
                scores[substance_name] = measurement.measurement
            # Populate Rescreening Details
            rescreening_data = {
                "gad_rescreening_interpretation": rescreening.gad_interpretation,
                "gad_rescreening_score": rescreening.gad_score,
                "phq_rescreening_interpretation": rescreening.phq_interpretation,
                "phq_rescreening_score": rescreening.phq_score,
                # Add logic to populate this field if available
                "suicidal_rescreening_interpretation": None,
                # Add logic to populate this field if available
                "suicidal_rescreening_score": None,
                "ace_rescreening_interpretation": rescreening.ace_interpretation,
                "ace_rescreening_score": rescreening.ace_score,
                "alcoholic_rescreening_interpretation": interpretations.get(
                    "Alcoholic", None
                ),
                "alcoholic_rescreening_score": scores.get("Alcoholic", None),
                "tobacco_rescreening_interpretation": interpretations.get(
                    "Tobacco", None
                ),
                "tobacco_rescreening_score": scores.get("Tobacco", None),
                "cannabis_rescreening_interpretation": interpretations.get(
                    "Cannabis", None
                ),
                "cannabis_rescreening_score": scores.get("Cannabis", None),
                "cocaine_rescreening_interpretation": interpretations.get(
                    "Cocaine", None
                ),
                "cocaine_rescreening_score": scores.get("Cocaine", None),
                "amphetamine_rescreening_interpretation": interpretations.get(
                    "Amphetamine", None
                ),
                "amphetamine_rescreening_score": scores.get("Amphetamine", None),
                "inhalants_rescreening_interpretation": interpretations.get(
                    "Inhalants", None
                ),
                "inhalants_rescreening_score": scores.get("Inhalants", None),
                "sedatives_rescreening_interpretation": interpretations.get(
                    "Sedatives", None
                ),
                "sedatives_rescreening_score": scores.get("Sedatives", None),
                "hallucinogens_rescreening_interpretation": interpretations.get(
                    "Hallucinogens", None
                ),
                "hallucinogens_rescreening_score": scores.get("Hallucinogens", None),
                "opioids_rescreening_interpretation": interpretations.get(
                    "Opioids", None
                ),
                "opioids_rescreening_score": scores.get("Opioids", None),
                "injection_rescreening_interpretation": interpretations.get(
                    "Injection", None
                ),
                "injection_rescreening_score": scores.get("Injection", None),
                "other_rescreening_interpretation": interpretations.get("Other", None),
                "other_rescreening_score": scores.get("Other", None),
                "other_rescreening_name": None,
            }

            # Save the updated data to the Rescreening instance
            for field, value in rescreening_data.items():
                setattr(rescreening, field, value)
            rescreening.save()

    return HttpResponse("User Archive Updated Successfully")
