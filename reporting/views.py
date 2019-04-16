from datetime import datetime, date
from django.contrib.auth.models import User as Token
from django.db.models import F, ExpressionWrapper, DateField
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group, Permission
from settings_module.models import Notification
from .models import Reporting, UserArchive
from measurement.models import Measurement, MeasurementAssist, UserSubmission, Submission
from monitoring.models import ServiceAndTreatment, Referral, Rescreening, Substance, SubstanceRiskMeasurement
from access.models import CustomUser, Agency, UserAgency
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.forms.models import model_to_dict
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def map_models(data):
    substance_dict = {}
    rescreening_dict = {}
    substance_risk_measurement_dict = {}

    # Mapping Substance objects
    for substance in data['substances']:
        substance_dict[substance.id] = substance.name

    # Mapping Rescreening objects
    for rescreening in data['rescreenings']:
        rescreening_dict[rescreening.id] = {
            'user': rescreening.user.username,
            'gad_data': rescreening.gad_data,
            'gad_score': rescreening.gad_score,
            'gad_interpretation': rescreening.gad_interpretation,
            'phq_data': rescreening.phq_data,
            'phq_score': rescreening.phq_score,
            'phq_interpretation': rescreening.phq_interpretation,
            'ace_data': rescreening.ace_data,
            'ace_score': rescreening.ace_score,
            'ace_interpretation': rescreening.ace_interpretation,
            'school_env_data': rescreening.school_env_data,
            'rescreened': rescreening.rescreened,
            'rescreening_count': rescreening.rescreening_count,
            'submission_date': rescreening.submission_date,
            'service_and_treatment_id': rescreening.service_and_treatment_id,
            'referral_id': rescreening.referral_id,
        }

    # Mapping SubstanceRiskMeasurement objects
    for measurement in data['substance_risk_measurements']:
        substance_risk_measurement_dict[measurement.id] = {
            'substance': substance_dict.get(measurement.substance_id),
            'rescreening': rescreening_dict.get(measurement.rescreening_id),
            'measurement': measurement.measurement,
            'risk_flag': measurement.risk_flag,
            'total_score': measurement.total_score,
        }

    return {
        'substances': substance_dict,
        'rescreenings': rescreening_dict,
        'substance_risk_measurements': substance_risk_measurement_dict,
    }

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

    # Fetching data for mapping
    data = {
        'substances': Substance.objects.all(),
        'rescreenings': Rescreening.objects.all(),
        'substance_risk_measurements': SubstanceRiskMeasurement.objects.all(),
    }
    mapped_data = map_models(data)

    for user in users_to_process:
        user_agency = UserAgency.objects.filter(user=user).first()
        user_submission = user.usersubmission_set.first()
        service_and_treatment = ServiceAndTreatment.objects.filter(user=user).first()
        
        # Check if a UserArchive instance with the same identity_number exists
        existing_user_archive = UserArchive.objects.filter(identity_number=user.identity_number).first()

        if user_agency:
            agency = user_agency.agency
            user_data = {
                'identity_number': user.identity_number,
                'nationality': user.nationality,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'mobile_number': user.mob_number,
                'is_gyalsung': user.is_gyalsung,
                'academy_code': user.academy_code,
                'role': user.role,
                'user_code': user_agency.user_code,
                'parent_status': user_agency.parent_status,
                'current_living_with': user_agency.current_living_with,
                'user_role_agency': user_agency.user_role_agency,
                'user_class': user_agency.user_class,
                'user_stream': user_agency.user_stream,
                'user_sub_class': user_agency.user_sub_class,
                'agency_code': agency.agency_code,
                'agency_name': agency.agency_name,
                'agency_parent': agency.agency_parent,
                'present_dzongkhag': agency.present_dzongkhag,
                'present_gewog': agency.present_gewog,
                'present_village': agency.present_village,
                'ps_add_village': user.ps_add_village,
                'ps_add_gewog': user.ps_add_gewog,
                'ps_add_dzongkhag': user.ps_add_dzongkhag,
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

        if user_submission:
            measurement = UserSubmission.objects.filter(user=user, user_submission=user_submission).first()
            
            if measurement:
                user_data = {
                    'gad_measurement': measurement.gad_measurement,
                    'gad_flag': measurement.gad_flag,
                    'phq_measurement': measurement.phq_measurement,
                    'phq_flag': measurement.phq_flag,
                    'suicidal_measurement': measurement.suicidal_measurement,
                    'suicidal_flag': measurement.suicidal_flag,
                    'ace_measurement': measurement.ace_measurement,
                    'ace_flag': measurement.ace_flag,
                    'overall_flag': measurement.overall_flag,
                    'alcoholic_measurement': measurement.assist.alcoholic_measurement if measurement.assist else None,
                    'alcoholic_flag': measurement.assist.alcoholic_flag if measurement.assist else None,
                    'tobacco_measurement': measurement.assist.tobacco_measurement if measurement.assist else None,
                    'tobacco_flag': measurement.assist.tobacco_flag if measurement.assist else None,
                    'cannabis_measurement': measurement.assist.cannabis_measurement if measurement.assist else None,
                    'cannabis_flag': measurement.assist.cannabis_flag if measurement.assist else None,
                    'cocaine_measurement': measurement.assist.cocaine_measurement if measurement.assist else None,
                    'cocaine_flag': measurement.assist.cocaine_flag if measurement.assist else None,
                    'amphetamine_measurement': measurement.assist.amphetamine_measurement if measurement.assist else None,
                    'amphetamine_flag': measurement.assist.amphetamine_flag if measurement.assist else None,
                    'inhalants_measurement': measurement.assist.inhalants_measurement if measurement.assist else None,
                    'inhalants_flag': measurement.assist.inhalants_flag if measurement.assist else None,
                    'sedatives_measurement': measurement.assist.sedatives_measurement if measurement.assist else None,
                    'sedatives_flag': measurement.assist.sedatives_flag if measurement.assist else None,
                    'hallucinogens_measurement': measurement.assist.hallucinogens_measurement if measurement.assist else None,
                    'hallucinogens_flag': measurement.assist.hallucinogens_flag if measurement.assist else None,
                    'opioids_measurement': measurement.assist.opioids_measurement if measurement.assist else None,
                    'opioids_flag': measurement.assist.opioids_flag if measurement.assist else None,
                    'injection_measurement': measurement.assist.injection_measurement if measurement.assist else None,
                    'injection_flag': measurement.assist.injection_flag if measurement.assist else None,
                    'other_measurement': measurement.assist.other_measurement if measurement.assist else None,
                    'other_flag': measurement.assist.other_flag if measurement.assist else None,
                    'other_name': measurement.assist.other_name if measurement.assist else None,
                    # Submission Details
                    'test_type': user_submission.test_type.name,
                    'rescreened': user_submission.rescreened,
                    'created_at': user_submission.created_at,
                }
                
                user_archive = UserArchive(**user_data)
                user_archive.save()

        if service_and_treatment:
            service_and_treatment_data = {
                'assessment_status': service_and_treatment.assessment_status,
                'case_status': service_and_treatment.case_status,
                'counseling': service_and_treatment.counseling,
                'follow_up': service_and_treatment.follow_up,
                'comments': service_and_treatment.comments,
                'updated_at': service_and_treatment.updated_at,
                'referred': service_and_treatment.referred,
            }

            for field, value in service_and_treatment_data.items():
                setattr(service_and_treatment, field, value)
            service_and_treatment.save()

        if referral_instance:
            for referral_instance in referral_instance:
                referral_data = {
                    'referred_by': referral_instance.referred_by,
                    'date': referral_instance.date,
                    'referred_to': referral_instance.referred_to,
                    'referred_to_name': referral_instance.referred_to_name,
                    'referral_status': referral_instance.referral_status,
                    'referral_remarks': referral_instance.referral_remarks,
                }

                # Update Referral Details
                for field, value in referral_data.items():
                    setattr(referral_instance, field, value)
                referral_instance.save()

    return HttpResponse("User Archive Updated Successfully")


def update_reporting_data(request):
    try:
        # Retrieve all UserSubmission records
        user_submissions = UserSubmission.objects.all()

        # Iterate through each UserSubmission and generate reports
        for user_submission in user_submissions:
            user = user_submission.user
            logger.info(f"Processing UserSubmission for user: {user}")

            # Retrieve related records
            measurement = Measurement.objects.filter(
                user_submission=user_submission).last()
            measurement_assist = MeasurementAssist.objects.filter(
                user_submission=user_submission).last()
            service_and_treatment = ServiceAndTreatment.objects.filter(
                user=user).last()
            referral = Referral.objects.filter(user=user).last()
            rescreening = Rescreening.objects.filter(user=user).last()
            user_agency = UserAgency.objects.filter(user=user).last()
            submission = Submission.objects.filter(
                user_submission=user_submission).first()

            diagnosis = submission.diagnosis if submission else None

            # Check if a Reporting record with identical details already exists
            existing_reports = Reporting.objects.filter(
                user=user,
                agency_code=user_agency.agency.agency_code if user_agency and user_agency.agency else None,
                # Add other fields for comparison as needed
            )

            if existing_reports.exists():
                logger.info(
                    f"Skipping UserSubmission for user {user}: Reporting record already exists")
                continue

            # Create a Reporting instance and populate fields directly
            reporting_record = Reporting(
                # User Details
                user=user,
                user_code=user.id,

                # User Agency Details
                agency_code=user_agency.agency.agency_code if user_agency and user_agency.agency else None,
                agency_name=user_agency.agency.agency_name if user_agency and user_agency.agency else None,
                parent_occupation=user_agency.parent_occupation if user_agency else None,
                guardian_name=user_agency.guardian_name if user_agency else None,
                guardian_occupation=user_agency.guardian_occupation if user_agency else None,
                parent_status=user_agency.parent_status if user_agency else None,
                current_living_with=user_agency.current_living_with if user_agency else None,
                user_role_agency=user_agency.user_role_agency if user_agency else None,
                user_class=user_agency.user_class if user_agency else None,
                user_stream=user_agency.user_stream if user_agency else None,
                user_sub_class=user_agency.user_sub_class if user_agency else None,

                # Present Address
                present_dzongkhag=user.perm_add_dzongkhag,
                present_gewog=user.perm_add_gewog,
                present_village=user.perm_add_village,

                # Past Diagnosis
                past_diagnosis=diagnosis,

                # Measurement and Assistance
                gad_measurement=measurement.gad_measurement if measurement else None,
                phq_measurement=measurement.phq_measurement if measurement else None,
                suicidal_measurement=measurement.suicidal_measurement if measurement else None,
                ace_measurement=measurement.ace_measurement if measurement else None,
                overall_flag=measurement.overall_flag if measurement else None,
                alcoholic_measurement=measurement_assist.alcoholic_measurement if measurement_assist else None,
                alcoholic_flag=measurement_assist.alcoholic_flag if measurement_assist else None,
                tobacco_measurement=measurement_assist.tobacco_measurement if measurement_assist else None,
                tobacco_flag=measurement_assist.tobacco_flag if measurement_assist else None,
                cannabis_measurement=measurement_assist.cannabis_measurement if measurement_assist else None,
                cannabis_flag=measurement_assist.cannabis_flag if measurement_assist else None,

                # Service and Treatment
                assessment_status=service_and_treatment.assessment_status if service_and_treatment else None,
                case_status=service_and_treatment.case_status if service_and_treatment else None,
                counseling=service_and_treatment.counseling if service_and_treatment else None,
                follow_up=service_and_treatment.follow_up if service_and_treatment else None,
                comments=service_and_treatment.comments if service_and_treatment else None,

                # Referral and Rescreening
                referral_status=referral.referral_status if referral else None,
                referral_remarks=referral.referral_remarks if referral else None,
                rescreening_count=rescreening.rescreening_count if rescreening else 0
            )

            # Save the Reporting instance
            reporting_record.save()
            logger.info(f"Reporting record saved for user: {user}")

        return JsonResponse({'message': 'Reporting data generated successfully for all users'})

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise


def get_reporting_data(request):
    reporting_data = Reporting.objects.all().select_related('user')

    # Convert queryset to list of dictionaries for JSON serialization
    reporting_list = []
    for reporting in reporting_data:
        # Calculate age based on date of birth
        dob = reporting.user.date_of_birth
        today = date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))

        # Format date
        created_at = reporting.created_at.strftime(
            '%Y-%m-%d') if reporting.created_at else 'NA'

        reporting_dict = {
            # Fields from Reporting model
            'user_id': reporting.user.id,
            'username': reporting.user.username,
            'agency_code': reporting.agency_code or 'NA',
            'agency_name': reporting.agency_name or 'NA',
            'present_dzongkhag': reporting.present_dzongkhag or 'NA',
            'present_gewog': reporting.present_gewog or 'NA',
            'present_village': reporting.present_village or 'NA',
            'user_code': reporting.user_code or 'NA',
            'parent_occupation': reporting.parent_occupation or 'NA',
            'guardian_name': reporting.guardian_name or 'NA',
            'guardian_occupation': reporting.guardian_occupation or 'NA',
            'parent_status': reporting.parent_status or 'NA',
            'current_living_with': reporting.current_living_with or 'NA',
            'user_role_agency': reporting.user_role_agency or 'NA',
            'user_class': reporting.user_class or 'NA',
            'user_stream': reporting.user_stream or 'NA',
            'user_sub_class': reporting.user_sub_class or 'NA',
            'past_diagnosis': reporting.past_diagnosis or 'NA',
            'gad_measurement': reporting.gad_measurement or 'NA',
            'phq_measurement': reporting.phq_measurement or 'NA',
            'suicidal_measurement': reporting.suicidal_measurement or 'NA',
            'ace_measurement': reporting.ace_measurement or 'NA',
            'overall_flag': reporting.overall_flag or 'NA',
            'alcoholic_measurement': reporting.alcoholic_measurement or 'NA',
            'alcoholic_flag': reporting.alcoholic_flag or 'NA',
            'tobacco_measurement': reporting.tobacco_measurement or 'NA',
            'tobacco_flag': reporting.tobacco_flag or 'NA',
            'cannabis_measurement': reporting.cannabis_measurement or 'NA',
            'cannabis_flag': reporting.cannabis_flag or 'NA',
            'cocaine_measurement': reporting.cocaine_measurement or 'NA',
            'cocaine_flag': reporting.cocaine_flag or 'NA',
            'amphetamine_measurement': reporting.amphetamine_measurement or 'NA',
            'amphetamine_flag': reporting.amphetamine_flag or 'NA',
            'inhalants_measurement': reporting.inhalants_measurement or 'NA',
            'inhalants_flag': reporting.inhalants_flag or 'NA',
            'sedatives_measurement': reporting.sedatives_measurement or 'NA',
            'sedatives_flag': reporting.sedatives_flag or 'NA',
            'hallucinogens_measurement': reporting.hallucinogens_measurement or 'NA',
            'hallucinogens_flag': reporting.hallucinogens_flag or 'NA',
            'opioids_measurement': reporting.opioids_measurement or 'NA',
            'opioids_flag': reporting.opioids_flag or 'NA',
            'injection_measurement': reporting.injection_measurement or 'NA',
            'injection_flag': reporting.injection_flag or 'NA',
            'other_measurement': reporting.other_measurement or 'NA',
            'other_flag': reporting.other_flag or 'NA',
            'other_name': reporting.other_name or 'NA',
            'assessment_status': reporting.assessment_status or 'NA',
            'case_status': reporting.case_status or 'NA',
            'counseling': reporting.counseling or 'NA',
            'follow_up': reporting.follow_up or 'NA',
            'comments': reporting.comments or 'NA',
            'referral_status': reporting.referral_status or 'NA',
            'referral_remarks': reporting.referral_remarks or 'NA',
            'rescreening_count': reporting.rescreening_count or 'NA',
            # User-specific fields
            'name': f"{reporting.user.first_name or ''} {reporting.user.middle_name or ''} {reporting.user.last_name or ''}".strip() or 'NA',
            'age': age or 'NA',
            'sex': reporting.user.gender or 'NA',
            # Date field
            'date': created_at
        }
        reporting_list.append(reporting_dict)

    # Return data as JSON response
    return JsonResponse(reporting_list, safe=False)


def orchestrate_reporting(request):
    try:
        logger.info("Orchestrating reporting process...")

        # Call the update_reporting_data function
        update_response = update_reporting_data(request)

        # Check if the update was successful
        if update_response.status_code == 200:
            logger.info("Reporting data update successful.")

            # If update was successful, call the get_reporting_data function
            reporting_response = get_reporting_data(request)
            logger.info("Reporting data retrieval successful.")

            # Return the JSON response from get_reporting_data function
            return reporting_response
        else:
            logger.error("Failed to update reporting data.")

            # If update failed, return the response from update_reporting_data function
            return JsonResponse({'error': 'Failed to update reporting data'}, status=update_response.status_code)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

        # Handle any unexpected errors
        return JsonResponse({'error': str(e)}, status=500)
