from datetime import date, datetime
import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from access.models import CustomUser
from measurement.models import UserSubmission
from .models import CaseBasedSubmission, CaseScreening, CaseSubstance, CaseSubstanceRiskMeasurement, EventBasedSubmission, EventScreening, EventSubstance, EventSubstanceRiskMeasurement
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def create_event_screening(request):
    try:
        # Log the incoming request
        logger.info(f"Received request: {request.method} {request.path}")
        logger.debug(f"Request body: {request.body}")

        # Assuming the JSON data is passed in the request body
        data = json.loads(request.body)

        # Validate required fields
        required_fields = ['event_name', 'location', 'start_date',
                           'end_date', 'duration', 'counselor', 'selected_tool']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

        # Create EventScreening object
        event_screening = EventScreening(
            event_name=data['event_name'],
            event_purpose=data.get('event_purpose', None),
            location=data['location'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            duration=data['duration'],
            counselor=data['counselor'],
            selected_tool=data['selected_tool']  # Include selected_tool
        )

        # Convert end_date to datetime.date object
        event_screening.end_date = datetime.strptime(
            event_screening.end_date, '%Y-%m-%d').date()

        # Save the object
        event_screening.save()
        logger.info("Event screening created successfully")

        return JsonResponse({'success': 'Event screening created successfully'}, status=201)

    except json.JSONDecodeError:
        logger.error("Invalid JSON data")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("An error occurred while creating event screening")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_counselor_info(request, counselor_name):
    try:
        # Get the last event for the counselor
        latest_event = EventScreening.objects.filter(
            counselor=counselor_name).last()

        if not latest_event:
            return JsonResponse({'message': 'Counselor information not available'}, status=200)

        # Check if registration lockout end time has passed
        if latest_event.registration_lockout_end_time and latest_event.registration_lockout_end_time <= timezone.now():
            # Update approval status to 'ended'
            latest_event.approval_status = 'ended'
            latest_event.save()

        counselor_info = {
            'event_name': latest_event.event_name,
            'event_purpose': latest_event.event_purpose,
            'location': latest_event.location,
            'start_date': latest_event.start_date,
            'end_date': latest_event.end_date,
            'duration': latest_event.duration,
            'approval_status': latest_event.approval_status,
            'remarks': latest_event.remarks,
            'rejection_reason': latest_event.rejection_reason,
            'selected_tool': latest_event.selected_tool
        }

        return JsonResponse(counselor_info, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def submit_case_screening(request):
    try:
        # Extract data from form data
        user_id = request.POST.get('userId')
        gad_data = request.POST.get('gadData')
        gad_score = request.POST.get('gadScore')
        gad_interpretation = request.POST.get('gadInterpretation')
        phq_data = request.POST.get('phqData')
        phq_score = request.POST.get('phqScore')
        phq_interpretation = request.POST.get('phqInterpretation')
        ace_data = request.POST.get('aceData')
        ace_score = request.POST.get('aceScore')
        ace_interpretation = request.POST.get('aceInterpretation')
        assist_risk_severity = request.POST.get('assistRiskSeverity')
        school_env_data = request.POST.get('schoolEnvData')

        # Retrieve the CustomUser instance based on the user ID
        user = get_object_or_404(CustomUser, pk=user_id)

        # Retrieve the latest CaseScreening for the user
        latest_case_screening = user.case_screenings.order_by('-date').first()

        # Create CaseBasedSubmission instance
        case_submission = CaseBasedSubmission.objects.create(
            user=user,
            case=latest_case_screening,  # Associate with the latest CaseScreening
            gad_data=gad_data,
            gad_score=gad_score,
            gad_interpretation=gad_interpretation,
            phq_data=phq_data,
            phq_score=phq_score,
            phq_interpretation=phq_interpretation,
            ace_data=ace_data,
            ace_score=ace_score,
            ace_interpretation=ace_interpretation,
            school_env_data=school_env_data
        )

        # Parse assist risk severity data
        assist_risk_severity = json.loads(assist_risk_severity)

        # Create CaseSubstanceRiskMeasurement instances
        for substance_name, severity in assist_risk_severity.items():
            # Check if the substance exists in the database
            substance, created = CaseSubstance.objects.get_or_create(name=substance_name)
            # Set a default value for the measurement field if it's not available from the request
            measurement = 0.0  # You can change this default value as needed
            CaseSubstanceRiskMeasurement.objects.create(
                substance=substance,
                case_submission=case_submission,
                measurement=measurement,  # Assign a default value
                risk_flag=severity
            )

        # Return success response
        return JsonResponse({'message': 'Submission saved successfully'})

    except Exception as e:
        # Log the exception
        logger.exception("Error occurred while processing submission")

        # Return error response
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_exempt
def submit_event_screening(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')

        # Retrieve the CustomUser instance using the provided user_id
        user = get_object_or_404(CustomUser, id=user_id)

        # Calculate the age of the user
        age = calculate_age(user.date_of_birth)

        # Updated key to match the sent data
        assist_data_json = request.POST.get('assistRiskSeverity')
        assist_data = json.loads(assist_data_json) if assist_data_json else {}

        # Start transaction to ensure data consistency
        with transaction.atomic():
            # Create or update the EventBasedSubmission instance
            eventscreening, created = EventBasedSubmission.objects.update_or_create(
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
                # Get the part after the space
                total_score_str = risk_level.split()[1]
                total_score = float(total_score_str.strip('()'))
                # Get the part before the space
                risk_flag = risk_level.split()[0]

                # Create Substance object if it doesn't exist
                substance_instance, _ = EventSubstance.objects.get_or_create(
                    name=substance)
                EventSubstanceRiskMeasurement.objects.create(
                    substance=substance_instance,
                    event_submission=eventscreening,
                    measurement=total_score,
                    risk_flag=risk_flag
                )

            # Set the rescreened field of the associated UserSubmission to True
            user_submission = UserSubmission.objects.get(user=user)
            if not user_submission.rescreened:
                user_submission.rescreened = True
                user_submission.save()

        if created:
            message = 'Event screening data saved successfully.'
        else:
            message = 'Event screening data updated successfully.'

        return JsonResponse({'message': message})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})


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
    }
