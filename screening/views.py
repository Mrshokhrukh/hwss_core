from datetime import date, datetime
import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from access.models import CustomUser
from django.utils.decorators import method_decorator
from measurement.models import UserSubmission
from .models import CaseBasedSubmission, CaseScreening, CaseSubstance, CaseSubstanceRiskMeasurement, EventBasedSubmission, EventScreening, EventSubstance, EventSubstanceRiskMeasurement
from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import EventBasedSubmissionSerializer, CaseBasedSubmissionSerializer

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
            'eventId': latest_event.pk,  # Add eventId to the response
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
        with transaction.atomic():
            user_id = request.POST.get('userId')
            gad_data = json.loads(request.POST.get('gadData', '{}'))
            phq_data = json.loads(request.POST.get('phqData', '{}'))
            ace_data = json.loads(request.POST.get('aceData', '{}'))
            assist_risk_severity = json.loads(request.POST.get('assistRiskSeverity', '{}'))
            school_env_data = json.loads(request.POST.get('schoolEnvData', '{}'))

            user = CustomUser.objects.get(pk=user_id)

            latest_case_screening = user.case_screenings.order_by('-date').first()
            if not latest_case_screening:
                # Optionally create a new case screening if none exists
                latest_case_screening = CaseScreening.objects.create(user=user, date=timezone.now())

            submission_instance = latest_case_screening.case_based_submissions.first()
            if submission_instance:
                submission_instance.gad_data = gad_data.get('responses', [])
                submission_instance.gad_score = gad_data.get('totalScore')
                submission_instance.gad_interpretation = gad_data.get('interpretation')
                submission_instance.phq_data = phq_data.get('responses', [])
                submission_instance.phq_score = phq_data.get('totalScore')
                submission_instance.phq_interpretation = phq_data.get('interpretation')
                submission_instance.ace_data = ace_data.get('responses', [])
                submission_instance.ace_score = ace_data.get('totalScore')
                submission_instance.ace_interpretation = ace_data.get('interpretation')
                submission_instance.school_env_data = school_env_data
                submission_instance.save()
            else:
                submission_instance = CaseBasedSubmission.objects.create(
                    user=user,
                    case=latest_case_screening,
                    gad_data=gad_data.get('responses', []),
                    gad_score=gad_data.get('totalScore'),
                    gad_interpretation=gad_data.get('interpretation'),
                    phq_data=phq_data.get('responses', []),
                    phq_score=phq_data.get('totalScore'),
                    phq_interpretation=phq_data.get('interpretation'),
                    ace_data=ace_data.get('responses', []),
                    ace_score=ace_data.get('totalScore'),
                    ace_interpretation=ace_data.get('interpretation'),
                    school_env_data=school_env_data
                )

            for substance_name, severity in assist_risk_severity.items():
                substance, _ = CaseSubstance.objects.get_or_create(name=substance_name)
                score = int(severity.split('(')[1].split(')')[0])
                CaseSubstanceRiskMeasurement.objects.create(
                    substance=substance,
                    case_submission=submission_instance,
                    measurement=0.0,
                    risk_flag=severity,
                    total_score=score
                )

        return JsonResponse({'message': 'Submission saved successfully'})

    except Exception as e:
        logger.exception(f"Error occurred while processing submission: {str(e)}")
        return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)



@csrf_exempt
def submit_event_screening(request):
    try:
        # Extract data from form data
        user_id = request.POST.get('userId')
        event_id = request.POST.get('eventId')
        gad_data = json.loads(request.POST.get('gadData', '{}'))
        phq_data = json.loads(request.POST.get('phqData', '{}'))
        ace_data = json.loads(request.POST.get('aceData', '{}'))
        assist_risk_severity = json.loads(
            request.POST.get('assistRiskSeverity', '{}'))
        school_env_data = json.loads(request.POST.get('schoolEnvData', '{}'))

        # Retrieve the CustomUser instance based on the user ID
        user = CustomUser.objects.get(pk=user_id)

        # Retrieve the EventScreening instance based on the event ID
        event = get_object_or_404(EventScreening, pk=event_id)

        # Create new EventBasedSubmission instance
        submission_instance = EventBasedSubmission.objects.create(
            user=user,
            event=event,
            gad_data=gad_data.get('responses', []),
            gad_score=gad_data.get('totalScore'),
            gad_interpretation=gad_data.get('interpretation'),
            phq_data=phq_data.get('responses', []),
            phq_score=phq_data.get('totalScore'),
            phq_interpretation=phq_data.get('interpretation'),
            ace_data=ace_data.get('responses', []),
            ace_score=ace_data.get('totalScore'),
            ace_interpretation=ace_data.get('interpretation'),
            school_env_data=school_env_data
        )

        # Create EventSubstanceRiskMeasurement instances
        for substance_name, severity in assist_risk_severity.items():
            # Check if the substance exists in the database
            substance, _ = EventSubstance.objects.get_or_create(
                name=substance_name)
            # Extract score from severity
            score = int(severity.split('(')[1].split(')')[0])
            # Create new instance
            EventSubstanceRiskMeasurement.objects.create(
                substance=substance,
                event_submission=submission_instance,
                measurement=0.0,  # Default value
                risk_flag=severity,
                total_score=score
            )

        # Return success response
        return JsonResponse({'message': 'Submission saved successfully'})

    except Exception as e:
        # Log the exception
        logger.exception("Error occurred while processing submission")

        # Return error response
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


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


@csrf_exempt
def get_event_screenings(request):
    if request.method == 'GET':
        events = EventScreening.objects.all()
        events_list = []

        for event in events:
            event_data = {
                'id': event.id,
                'event_name': event.event_name,
                'event_purpose': event.event_purpose,
                'location': event.location,
                'start_date': event.start_date,
                'end_date': event.end_date,
                'duration': event.duration,
                'counselor': event.counselor,
                'approval_status': event.approval_status,
                'remarks': event.remarks,
                'rejection_reason': event.rejection_reason,
                'registration_lockout_end_time': event.registration_lockout_end_time,
                'selected_tool': event.selected_tool,
                # Adjust the fields as needed
                'users': list(event.users.values('id', 'username', 'email'))
            }
            events_list.append(event_data)

        return JsonResponse(events_list, safe=False)


@csrf_exempt
def update_event_screening(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            approval_status = data.get('approval_status')
            rejection_reason = data.get('rejection_reason', None)

            if not event_id or not approval_status:
                return JsonResponse({'error': 'Invalid request. event_id and approval_status are required.'}, status=400)

            event = get_object_or_404(EventScreening, pk=event_id)

            event.approval_status = approval_status
            if approval_status == 'rejected' and rejection_reason:
                event.rejection_reason = rejection_reason
            else:
                event.rejection_reason = None

            event.save()
            return JsonResponse({'message': 'Event updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.exception("Error occurred while updating event screening")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# EventBasedRecordViewSet
@method_decorator(csrf_exempt, name='dispatch')
class EventBasedRecordViewSet(viewsets.ModelViewSet):
    queryset = EventBasedSubmission.objects.all().prefetch_related(
        'user', 'event', 'service_and_treatment', 'referral',
        Prefetch('event_substance_risk_measurements', queryset=EventSubstanceRiskMeasurement.objects.all())
    )
    serializer_class = EventBasedSubmissionSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def full_event_records(self, request):
        submissions = self.get_queryset()
        response_data = []

        for submission in submissions:
            user = submission.user
            event = submission.event
            risk_measurements = submission.event_substance_risk_measurements.all()

            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'event': {
                    'event_name': event.event_name,
                    'event_purpose': event.event_purpose,
                    'location': event.location,
                    'duration': event.duration,
                },
                'submission': {
                    'gad_score': submission.gad_score,
                    'phq_score': submission.phq_score,
                    'ace_score': submission.ace_score,
                    'service_and_treatment': submission.service_and_treatment.name if submission.service_and_treatment else None,
                    'referral': submission.referral.referral_type if submission.referral else None,
                },
                'substance_risk_measurements': [
                    {
                        'substance': risk.substance.name,
                        'measurement': risk.measurement,
                        'risk_flag': risk.risk_flag,
                        'total_score': risk.total_score,
                    } for risk in risk_measurements
                ]
            }

            response_data.append(data)

        return Response(response_data)

# CaseBasedRecordViewSet
@method_decorator(csrf_exempt, name='dispatch')
class CaseBasedRecordViewSet(viewsets.ModelViewSet):
    queryset = CaseBasedSubmission.objects.all().prefetch_related(
        'user', 'case', 'service_and_treatment', 'referral',
        Prefetch('case_substance_risk_measurements', queryset=CaseSubstanceRiskMeasurement.objects.all())
    )
    serializer_class = CaseBasedSubmissionSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def full_case_records(self, request):
        submissions = self.get_queryset()
        response_data = []

        for submission in submissions:
            user = submission.user
            case = submission.case
            risk_measurements = submission.case_substance_risk_measurements.all()

            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'case': {
                    'case_name': case.case_name,
                    'purpose': case.purpose,
                    'dzongkhag': case.dzongkhag,
                    'date': case.date,
                },
                'submission': {
                    'gad_score': submission.gad_score,
                    'phq_score': submission.phq_score,
                    'ace_score': submission.ace_score,
                    'service_and_treatment': submission.service_and_treatment.name if submission.service_and_treatment else None,
                    'referral': submission.referral.referral_type if submission.referral else None,
                },
                'substance_risk_measurements': [
                    {
                        'substance': risk.substance.name,
                        'measurement': risk.measurement,
                        'risk_flag': risk.risk_flag,
                        'total_score': risk.total_score,
                    } for risk in risk_measurements
                ]
            }

            response_data.append(data)

        return Response(response_data)