from django.http import JsonResponse
from .models import Reporting
from measurement.models import Measurement, MeasurementAssist, UserSubmission, Submission
from monitoring.models import ServiceAndTreatment, Referral, Rescreening
from access.models import CustomUser, Agency, UserAgency
from django.core.exceptions import ObjectDoesNotExist
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def update_reporting_data(request):
    try:
        # Retrieve all UserSubmission records
        user_submissions = UserSubmission.objects.all()

        # Iterate through each UserSubmission and generate reports
        for user_submission in user_submissions:
            user = user_submission.user
            logger.info(f"Processing UserSubmission for user: {user}")

            # Retrieve related records
            measurement = Measurement.objects.filter(user_submission=user_submission).last()
            measurement_assist = MeasurementAssist.objects.filter(user_submission=user_submission).last()
            service_and_treatment = ServiceAndTreatment.objects.filter(user=user).last()
            referral = Referral.objects.filter(user=user).last()
            rescreening = Rescreening.objects.filter(user=user).last()
            user_agency = UserAgency.objects.filter(user=user).last()
            submission = Submission.objects.filter(user_submission=user_submission).first()

            diagnosis = submission.diagnosis if submission else None

            # Check if a Reporting record with identical details already exists
            existing_reports = Reporting.objects.filter(
                user=user,
                agency_code=user_agency.agency.agency_code if user_agency and user_agency.agency else None,
                # Add other fields for comparison as needed
            )

            if existing_reports.exists():
                logger.info(f"Skipping UserSubmission for user {user}: Reporting record already exists")
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
                rescreening_count=rescreening.rescreening_count if rescreening else None
            )

            # Save the Reporting instance
            reporting_record.save()
            logger.info(f"Reporting record saved for user: {user}")

        return JsonResponse({'message': 'Reporting data generated successfully for all users'})

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise



def get_reporting_data(request):
    reporting_data = Reporting.objects.all()

    # Convert queryset to list of dictionaries for JSON serialization
    reporting_list = []
    for reporting in reporting_data:
        reporting_dict = {
            'user_id': reporting.user.id,
            'username': reporting.user.username,
            'agency_code': reporting.agency_code,
            'agency_name': reporting.agency_name,
            'present_dzongkhag': reporting.present_dzongkhag,
            'present_gewog': reporting.present_gewog,
            'present_village': reporting.present_village,
            'user_code': reporting.user_code,
            'parent_occupation': reporting.parent_occupation,
            'guardian_name': reporting.guardian_name,
            'guardian_occupation': reporting.guardian_occupation,
            'parent_status': reporting.parent_status,
            'current_living_with': reporting.current_living_with,
            'user_role_agency': reporting.user_role_agency,
            'user_class': reporting.user_class,
            'user_stream': reporting.user_stream,
            'user_sub_class': reporting.user_sub_class,
            'past_diagnosis': reporting.past_diagnosis,
            'gad_measurement': reporting.gad_measurement,
            'phq_measurement': reporting.phq_measurement,
            'suicidal_measurement': reporting.suicidal_measurement,
            'ace_measurement': reporting.ace_measurement,
            'overall_flag': reporting.overall_flag,
            'alcoholic_measurement': reporting.alcoholic_measurement,
            'alcoholic_flag': reporting.alcoholic_flag,
            'tobacco_measurement': reporting.tobacco_measurement,
            'tobacco_flag': reporting.tobacco_flag,
            'cannabis_measurement': reporting.cannabis_measurement,
            'cannabis_flag': reporting.cannabis_flag,
            'cocaine_measurement': reporting.cocaine_measurement,
            'cocaine_flag': reporting.cocaine_flag,
            'amphetamine_measurement': reporting.amphetamine_measurement,
            'amphetamine_flag': reporting.amphetamine_flag,
            'inhalants_measurement': reporting.inhalants_measurement,
            'inhalants_flag': reporting.inhalants_flag,
            'sedatives_measurement': reporting.sedatives_measurement,
            'sedatives_flag': reporting.sedatives_flag,
            'hallucinogens_measurement': reporting.hallucinogens_measurement,
            'hallucinogens_flag': reporting.hallucinogens_flag,
            'opioids_measurement': reporting.opioids_measurement,
            'opioids_flag': reporting.opioids_flag,
            'injection_measurement': reporting.injection_measurement,
            'injection_flag': reporting.injection_flag,
            'other_measurement': reporting.other_measurement,
            'other_flag': reporting.other_flag,
            'other_name': reporting.other_name,
            'assessment_status': reporting.assessment_status,
            'case_status': reporting.case_status,
            'counseling': reporting.counseling,
            'follow_up': reporting.follow_up,
            'comments': reporting.comments,
            'referral_status': reporting.referral_status,
            'referral_remarks': reporting.referral_remarks,
            'rescreening_count': reporting.rescreening_count,
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
