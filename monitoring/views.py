from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from measurement.models import Measurement, MeasurementAssist, UserSubmission
from django.views.decorators.csrf import csrf_exempt
from access.models import CustomUser
from .models import Rescreening, ServiceAndTreatment, Referral
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def save_to_rescreening(request):
    users = CustomUser.objects.all()

    for user in users:
        submissions = UserSubmission.objects.filter(user=user)

        for submission in submissions:
            measurement_entry = Measurement.objects.filter(
                Q(phq_flag='yellow') | Q(gad_flag='yellow'), user_submission=submission).first()
            assist_entry = MeasurementAssist.objects.filter(
                Q(alcoholic_flag='yellow') | Q(tobacco_flag='yellow') | Q(cannabis_flag='yellow') | Q(
                    cocaine_flag='yellow') | Q(amphetamine_flag='yellow') | Q(inhalants_flag='yellow') | Q(
                    sedatives_flag='yellow') | Q(hallucinogens_flag='yellow') | Q(opioids_flag='yellow') | Q(
                    other_flag='yellow'), user_submission=submission).first()

            if measurement_entry or assist_entry:
                submission_data = {
                    'submission_id': submission.id,
                    'submission_date': submission.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'diagnosis': submission.submissions.first().diagnosis if submission.submissions.exists() else None
                }

                measurement_data = {
                    'phq_measurement': measurement_entry.phq_measurement if measurement_entry else None,
                    'phq_flag': measurement_entry.phq_flag if measurement_entry else None,
                    'gad_measurement': measurement_entry.gad_measurement if measurement_entry else None,
                    'gad_flag': measurement_entry.gad_flag if measurement_entry else None,
                }

                measurement_assist_data = {
                    'alcoholic_measurement': assist_entry.alcoholic_measurement if assist_entry else None,
                    'alcoholic_flag': assist_entry.alcoholic_flag if assist_entry else None,
                    'tobacco_measurement': assist_entry.tobacco_measurement if assist_entry else None,
                    'tobacco_flag': assist_entry.tobacco_flag if assist_entry else None,
                    'cannabis_measurement': assist_entry.cannabis_measurement if assist_entry else None,
                    'cannabis_flag': assist_entry.cannabis_flag if assist_entry else None,
                    'cocaine_measurement': assist_entry.cocaine_measurement if assist_entry else None,
                    'cocaine_flag': assist_entry.cocaine_flag if assist_entry else None,
                    'amphetamine_measurement': assist_entry.amphetamine_measurement if assist_entry else None,
                    'amphetamine_flag': assist_entry.amphetamine_flag if assist_entry else None,
                    'inhalants_measurement': assist_entry.inhalants_measurement if assist_entry else None,
                    'inhalants_flag': assist_entry.inhalants_flag if assist_entry else None,
                    'sedatives_measurement': assist_entry.sedatives_measurement if assist_entry else None,
                    'sedatives_flag': assist_entry.sedatives_flag if assist_entry else None,
                    'hallucinogens_measurement': assist_entry.hallucinogens_measurement if assist_entry else None,
                    'hallucinogens_flag': assist_entry.hallucinogens_flag if assist_entry else None,
                    'opioids_measurement': assist_entry.opioids_measurement if assist_entry else None,
                    'opioids_flag': assist_entry.opioids_flag if assist_entry else None,
                    'injection_measurement': assist_entry.injection_measurement if assist_entry else None,
                    'injection_flag': assist_entry.injection_flag if assist_entry else None,
                    'other_measurement': assist_entry.other_measurement if assist_entry else None,
                    'other_flag': assist_entry.other_flag if assist_entry else None,
                }

                # Check if a duplicate record exists in Rescreening
                existing_rescreening = Rescreening.objects.filter(
                    user=user, submission_diagnosis=submission_data['diagnosis']).exists()

                # If no duplicate record, save data to Rescreening model
                if not existing_rescreening:
                    Rescreening.objects.create(
                        user=user,
                        submission_diagnosis=submission_data['diagnosis'],
                        measurement=measurement_data,
                        measurement_assist=measurement_assist_data
                    )
                logger.debug(
                    f"Saved rescreening data for user: {user.username}, submission: {submission.id}")


@csrf_exempt
def get_rescreening_records(request):
    rescreening_records = Rescreening.objects.filter(rescreening_count=0)
    
    result = {}

    for record in rescreening_records:
        user_data = {
            'id': record.user.id,
            'username': record.user.username,
            'identity_number': record.user.identity_number,
            'nationality': record.user.nationality,
            'first_name': record.user.first_name,
            'middle_name': record.user.middle_name,
            'last_name': record.user.last_name,
            'date_of_birth': record.user.date_of_birth.strftime('%Y-%m-%d'),
            'gender': record.user.gender,
            'email': record.user.email,
            'mob_number': record.user.mob_number,
            'father_name': record.user.father_name,
            'mother_name': record.user.mother_name,
            'active_agency': record.user.active_agency.agency_name if record.user.active_agency else None,
            'ps_add_dzongkhag': record.user.ps_add_dzongkhag,
            'is_gyalsung': record.user.is_gyalsung,
            'role': record.user.role,
        }

        submission_data = {
            'diagnosis': record.submission_diagnosis,
            'submission_date': record.date,
        }

        measurement_data = record.measurement
        measurement_assist_data = record.measurement_assist

        result.setdefault(
            record.user.id, {'user_data': user_data, 'submission_details': []})
        result[record.user.id]['submission_details'].append({
            'submission_data': submission_data,
            'measurement_data': measurement_data,
            'measurement_assist_data': measurement_assist_data
        })

    return JsonResponse({'flag_details': list(result.values())}, status=200)


@csrf_exempt
def process_rescreening(request):
    # Trigger saving of records to Rescreening table
    save_to_rescreening(request)
    logger.debug("Saved rescreening data")

    # Retrieve saved records from Rescreening table
    rescreening_records = get_rescreening_records(request)

    # Log the data being returned
    logger.debug("Response data:")
    logger.debug(rescreening_records)

    # Return the JsonResponse object directly
    return rescreening_records


def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - \
        ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def getServiceAndTreatmentList(request):
    service_and_treatment_data = []
    service_and_treatments = ServiceAndTreatment.objects.all()

    for service_and_treatment in service_and_treatments:
        birth_date = service_and_treatment.user.date_of_birth
        age = calculate_age(birth_date)

        user_data = {
            'date_of_birth': birth_date.strftime('%Y-%m-%d'),
            'name': f"{service_and_treatment.user.first_name} {service_and_treatment.user.middle_name} {service_and_treatment.user.last_name}",
            'age': age,
            'gender': service_and_treatment.user.gender,
        }

        service_and_treatment_entry = {
            'user_data': user_data,
            'date': service_and_treatment.date.strftime('%Y-%m-%d'),
            'case_status': service_and_treatment.case_status,
            'assessment_status': service_and_treatment.assessment_status,
            'counseling': service_and_treatment.counseling,
            'follow_up': service_and_treatment.follow_up,
            'comments': service_and_treatment.comments,
        }

        service_and_treatment_data.append(service_and_treatment_entry)

    return JsonResponse({'service_and_treatment_data': service_and_treatment_data}, status=200)


@csrf_exempt
@require_POST
def update_service_and_treatment(request):
    try:
        data = json.loads(request.body)
        service_and_treatment_id = data.get('service_and_treatment_id')
        updated_fields = data.get('updated_fields', {})

        # Ensure both service_and_treatment_id and updated_fields are provided
        if not service_and_treatment_id or not updated_fields:
            return JsonResponse({'error': 'Invalid request. Please provide service_and_treatment_id and updated_fields'}, status=400)

        # Fetch the ServiceAndTreatment object to update
        service_and_treatment = ServiceAndTreatment.objects.get(
            pk=service_and_treatment_id)

        # Update the fields based on the provided data
        for field, value in updated_fields.items():
            setattr(service_and_treatment, field, value)

        # Save the changes
        service_and_treatment.save()

        return JsonResponse({'message': 'ServiceAndTreatment updated successfully'}, status=200)

    except ServiceAndTreatment.DoesNotExist:
        return JsonResponse({'error': 'ServiceAndTreatment does not exist'}, status=404)


def getReferralList(request):
    referrals = Referral.objects.all()
    referral_list = []

    for referral in referrals:
        birth_date = referral.user.date_of_birth
        age = calculate_age(birth_date)

        user_data = {
            'date_of_birth': birth_date.strftime('%Y-%m-%d'),
            'name': f"{referral.user.first_name} {referral.user.middle_name} {referral.user.last_name}",
            'age': age,
            'gender': referral.user.gender,
        }

        referral_data = {
            'user_data': user_data,
            'referred_by': {
                'username': referral.referred_by.username if referral.referred_by else None
            },
            'referred_to': {
                'name': referral.referred_to_name
            },
            'date': referral.date,
            'referral_status': referral.referral_status,
            'referral_remarks': referral.referral_remarks,
        }
        referral_list.append(referral_data)

    return JsonResponse({'referral_list': referral_list}, status=200)


@csrf_exempt
@require_POST
def updateReferralStatus(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            referral_id = data.get('referral_id')
            new_status = data.get('new_status')

            # Ensure both referral_id and new_status are provided
            if not referral_id or not new_status:
                return JsonResponse({'error': 'Invalid request. Please provide referral_id and new_status'}, status=400)

            # Fetch the Referral object to update
            referral = Referral.objects.get(pk=referral_id)

            # Update the referral status
            referral.referral_status = new_status
            referral.save()

            return JsonResponse({'message': 'Referral status updated successfully'}, status=200)

        except Referral.DoesNotExist:
            return JsonResponse({'error': 'Referral does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST requests are allowed'}, status=405)
