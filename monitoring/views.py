from datetime import date
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from measurement.models import Measurement, MeasurementAssist, Submission, UserSubmission
from django.views.decorators.csrf import csrf_exempt
from access.models import CustomUser, UserAgency
from .models import Rescreening, ServiceAndTreatment, Referral, Substance, SubstanceRiskMeasurement
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
from django.views.decorators.http import require_GET
from django.forms.models import model_to_dict
from django.db import transaction
from datetime import date
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def submit_rescreening(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')

        # Retrieve the CustomUser instance using the provided user_id
        user = get_object_or_404(CustomUser, id=user_id)

        # Calculate the age of the user
        age = calculate_age(user.date_of_birth)

        assist_data_json = request.POST.get('assistRiskSeverity')  # Updated key to match the sent data
        assist_data = json.loads(assist_data_json) if assist_data_json else {}

        # Start transaction to ensure data consistency
        with transaction.atomic():
            # Create or update the Rescreening instance
            rescreening, created = Rescreening.objects.update_or_create(
                user=user,
                defaults={
                    'gad_data': request.POST.get('gadData', {}),
                    'gad_score': json.loads(request.POST.get('gadData', '{}')).get('totalScore', 0),
                    'phq_data': request.POST.get('phqData', {}),
                    'phq_score': json.loads(request.POST.get('phqData', '{}')).get('totalScore', 0),
                    'ace_data': request.POST.get('aceData', {}),
                    'ace_score': json.loads(request.POST.get('aceData', '{}')).get('totalScore', 0),
                    'school_env_data': request.POST.get('schoolEnvData', {}),
                    'rescreened': True
                }
            )

            # Save substance risk measurements
            for substance, risk_level in assist_data.items():
                # Extract total score and risk flag from the risk level string
                total_score_str = risk_level.split()[1]  # Get the part after the space
                total_score = float(total_score_str.strip('()'))  # Remove parentheses and convert to float
                risk_flag = risk_level.split()[0]  # Get the part before the space

                # Create Substance object if it doesn't exist
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

        if created:
            message = 'Rescreening data saved successfully.'
        else:
            message = 'Rescreening data updated successfully.'

        return JsonResponse({'message': message})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})


def get_non_green_flags(request):
    rescreening_list = []

    # Iterate over all UserSubmission instances
    for submission in UserSubmission.objects.filter(rescreened=False):
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
    return {
        'id': user.id,
        'full_name': f"{user.first_name} {user.middle_name or ''} {user.last_name}",
        'age': (timezone.now().date() - user.date_of_birth).days // 365,
        'gender': user.gender,
        # Add other fields as needed
    }


def generateServiceAndTreatment(request):
    try:
        # Retrieve all rescreenings
        rescreenings = Rescreening.objects.all()

        # List to store the created ServiceAndTreatment instances
        service_and_treatments_created = []

        # Loop through each rescreening
        for rescreening in rescreenings:
            existing_instance = ServiceAndTreatment.objects.filter(
                user=rescreening.user,
                date=rescreening.submission_date.date(),
            ).exists()

            # If no existing instance found, create and save a new one
            if not existing_instance:
                service_and_treatment = ServiceAndTreatment.objects.create(
                    user=rescreening.user,
                    date=rescreening.submission_date.date(),
                    assessment_status='Not Conducted',
                    case_status='On Going',
                    counseling='Waiting List',
                    follow_up='',
                    comments='',
                )
                service_and_treatment.save()

                # Append the created ServiceAndTreatment instance to the list
                service_and_treatments_created.append(service_and_treatment)

                # Update the rescreening to mark it as rescreened
                rescreening.rescreened = True
                rescreening.save()

        # Retrieve all instances of ServiceAndTreatment
        service_and_treatments = ServiceAndTreatment.objects.all()

        # Serialize the ServiceAndTreatment instances along with user details to JSON
        service_and_treatments_data = [{
            'user': get_user_details(obj.user),
            'date': obj.date,
            'assessment_status': obj.assessment_status,
            'case_status': obj.case_status,
            'counseling': obj.counseling,
            'follow_up': obj.follow_up,
            'comments': obj.comments,
        } for obj in service_and_treatments]

        return JsonResponse({'message': 'ServiceAndTreatment records updated successfully', 'data': service_and_treatments_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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


# function for getting users details:
def get_user_monitoring_details(request):
    # Retrieve the user ID from query parameters
    user_id = request.GET.get('user_id')

    # Check if user_id is provided
    if user_id is None:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    # Retrieve the user object based on the user ID
    user = get_object_or_404(CustomUser, pk=user_id)

    # Retrieve the user's agency details
    try:
        user_agency = UserAgency.objects.get(user=user)
        agency_details = {
            'agency_name': user_agency.agency.agency_name,
            'agency_code': user_agency.agency.agency_code,
            'agency_parent': user_agency.agency.agency_parent,
            'present_dzongkhag': user_agency.agency.present_dzongkhag,
            'present_gewog': user_agency.agency.present_gewog,
            'present_village': user_agency.agency.present_village,
            # Add other agency details as needed
        }
    except UserAgency.DoesNotExist:
        agency_details = None

    # Retrieve service and treatment details for the user
    service_and_treatment_details = list(
        ServiceAndTreatment.objects.filter(user=user).values())

    # Retrieve referral details for the user
    referral_details = list(Referral.objects.filter(user=user).values())

    # Retrieve rescreening details for the user
    rescreenings = Rescreening.objects.filter(user=user)
    rescreening_details = []
    for rescreening in rescreenings:
        rescreening_data = {
            'id': rescreening.id,
            'submission_date': rescreening.submission_date.strftime('%Y-%m-%d %H:%M:%S'),
            # Include other relevant fields here
        }
        rescreening_details.append(rescreening_data)

    # Retrieve SubstanceRiskMeasurement details for the user
    substance_risk_measurements = SubstanceRiskMeasurement.objects.filter(rescreening__in=rescreenings)
    substance_risk_measurement_details = []
    for measurement in substance_risk_measurements:
        substance_name = measurement.substance.name  # Fetch the name of the substance
        measurement_data = {
            'id': measurement.id,
            'substance_name': substance_name,
            'measurement': measurement.measurement,
            'risk_flag': measurement.risk_flag,
            'total_score': measurement.total_score,
            # Include other relevant fields here
        }
        substance_risk_measurement_details.append(measurement_data)

    # Construct the user details JSON response
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
    }

    return JsonResponse(user_details)
