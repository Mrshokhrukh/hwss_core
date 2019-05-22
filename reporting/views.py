from datetime import datetime, date
from django.contrib.auth.models import User as Token
from django.db.models import F, ExpressionWrapper, DateField
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group, Permission
from screening.models import CaseBasedSubmission, CaseScreening, CaseSubstanceRiskMeasurement, EventBasedSubmission, EventScreening, EventSubstanceRiskMeasurement, ScreenedUser
from settings_module.models import Notification
from .models import Reporting, ReportingModel
from measurement.models import Measurement, MeasurementAssist, UserSubmission, Submission
from monitoring.models import ServiceAndTreatment, Referral, Rescreening, Substance, SubstanceRiskMeasurement
from access.models import CustomUser, Agency, UserAgency
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.forms.models import model_to_dict
import logging
from django.core.serializers import serialize

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


def populate_reporting_model():
    # Filter users with specified roles
    users = CustomUser.objects.filter(role__in=['student', 'general_public'])

    for user in users:
        # Retrieve active agency or user agency
        user_agency = None
        agency_name = None

        try:
            user_agency = UserAgency.objects.get(user=user)
            agency_name = user_agency.agency.agency_name
        except UserAgency.DoesNotExist:
            print(f"No UserAgency found for user: {user.username}")
            pass

        print(f"User: {user.username}, UserAgency: {user_agency}, Agency Name: {agency_name}")

        # Create a ReportingModel instance for each user
        reporting_model, created = ReportingModel.objects.get_or_create(
            user=user,
            defaults={
                'user_agency': user_agency,
                'agency_name': agency_name,
                'service_and_treatment': None,
                'referral': None,
                'measurement': None,
                'measurement_assist': None,
                'rescreened': False,
                'isMarkedSafe': False,  # Adding the new field here
                'original_submission_date': None,
                'rescreening_data': None,
            }
        )

        # Retrieve other information and associate with ReportingModel
        latest_submission = UserSubmission.objects.filter(user=user).order_by('-created_at').first()
        if latest_submission:
            reporting_model.original_submission_date = latest_submission.created_at
            reporting_model.rescreened = latest_submission.rescreened
            reporting_model.isMarkedSafe = latest_submission.mark_as_safe  # Assigning the new field here

            latest_measurement = Measurement.objects.filter(user_submission=latest_submission).last()
            if latest_measurement:
                reporting_model.measurement = latest_measurement

            latest_measurement_assist = MeasurementAssist.objects.filter(user=user, user_submission=latest_submission).last()
            if latest_measurement_assist:
                reporting_model.measurement_assist = latest_measurement_assist

            latest_rescreening_data = Rescreening.objects.filter(user=user).last()
            if latest_rescreening_data:
                reporting_model.rescreening_data = latest_rescreening_data

            # Add foreign key relationships from the screening app
            reporting_model.case_screenings.set(CaseScreening.objects.filter(user=user))
            reporting_model.screened_users.set(ScreenedUser.objects.filter(user=user))
            reporting_model.case_based_submissions.set(CaseBasedSubmission.objects.filter(user=user))
            reporting_model.case_substance_risk_measurements.set(CaseSubstanceRiskMeasurement.objects.filter(case_submission__user=user))
            reporting_model.event_screenings.set(EventScreening.objects.filter(users=user))
            reporting_model.event_based_submissions.set(EventBasedSubmission.objects.filter(user=user))
            reporting_model.event_substance_risk_measurements.set(EventSubstanceRiskMeasurement.objects.filter(event_submission__user=user))

        # Save the ReportingModel instance
        reporting_model.save()



def populate_reporting_model_view(request):
    try:
        populate_reporting_model()
        return JsonResponse({'status': 'success', 'message': 'ReportingModel populated successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    


def get_reporting_model_data(request):
    # Retrieve all ReportingModel instances along with related data
    reporting_models = ReportingModel.objects.select_related(
        'user_agency', 'agency', 'service_and_treatment', 'referral', 'measurement', 'measurement_assist', 'rescreened_by'
    ).prefetch_related(
        'case_screenings', 'screened_users', 'case_based_submissions', 'case_substance_risk_measurements',
        'event_screenings', 'event_based_submissions', 'event_substance_risk_measurements'
    ).all()

    # Convert queryset to list of dictionaries including related object data
    reporting_model_data = []
    for reporting_model in reporting_models:
        service_and_treatment = reporting_model.service_and_treatment
        if service_and_treatment:
            service_and_treatment_data = {
                'id': service_and_treatment.id,
                'user': service_and_treatment.user_id,
                'date': service_and_treatment.date,
                'assessment_status': service_and_treatment.assessment_status,
                'case_status': service_and_treatment.case_status,
                'counseling': service_and_treatment.counseling,
                'follow_up': service_and_treatment.follow_up,
                'comments': service_and_treatment.comments,
                'updated_by': service_and_treatment.updated_by_id,
                'updated_at': service_and_treatment.updated_at,
                'referred': service_and_treatment.referred,
                'referral_instance': service_and_treatment.referral_instance_id,
            }
        else:
            service_and_treatment_data = None

        data = {
            'userId': reporting_model.pk,
            'user': serialize('json', [reporting_model.user]) if reporting_model.user else None,
            'user_agency': serialize('json', [reporting_model.user_agency]) if reporting_model.user_agency else None,
            'agency': serialize('json', [reporting_model.agency]) if reporting_model.agency else None,
            'agency_name': reporting_model.agency_name,
            'service_and_treatment': json.dumps(service_and_treatment_data),
            'referral': serialize('json', [reporting_model.referral]) if reporting_model.referral else None,
            'measurement': serialize('json', [reporting_model.measurement]) if reporting_model.measurement else None,
            'measurement_assist': serialize('json', [reporting_model.measurement_assist]) if reporting_model.measurement_assist else None,
            'rescreened': reporting_model.rescreened,
            'rescreened_by': serialize('json', [reporting_model.rescreened_by]) if reporting_model.rescreened_by else None,
            'original_submission_date': reporting_model.original_submission_date,
            'rescreened_date': reporting_model.rescreened_date,
            'case_screenings': serialize('json', reporting_model.case_screenings.all()),
            'screened_users': serialize('json', reporting_model.screened_users.all()),
            'case_based_submissions': serialize('json', reporting_model.case_based_submissions.all()),
            'case_substance_risk_measurements': serialize('json', reporting_model.case_substance_risk_measurements.all()),
            'event_screenings': serialize('json', reporting_model.event_screenings.all()),
            'event_based_submissions': serialize('json', reporting_model.event_based_submissions.all()),
            'event_substance_risk_measurements': serialize('json', reporting_model.event_substance_risk_measurements.all()),
            'rescreening_data': serialize('json', [reporting_model.rescreening_data]) if reporting_model.rescreening_data else None,
        }
        reporting_model_data.append(data)

    # Return the JSON response
    return JsonResponse(reporting_model_data, safe=False)