from datetime import date, datetime
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from access.models import CustomUser
from django.utils.decorators import method_decorator
from measurement.models import UserSubmission
from monitoring.models import Notification
from .models import CaseBasedSubmission, CaseScreening, CaseSubstance, CaseSubstanceRiskMeasurement, EventBasedSubmission, EventScreening, EventSubstance, EventSubstanceRiskMeasurement
from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import EventBasedSubmissionSerializer, CaseBasedSubmissionSerializer
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def create_event_screening(request):
    """
    Handles the creation of a new event screening and notifies all admins.
    - mh_admins receive an actionable notification to approve/reject.
    - sud_admins receive an informational notification.
    """
    try:
        data = json.loads(request.body)
        required_fields = ['event_name', 'location', 'start_date',
                           'end_date', 'duration', 'created_by', 'selected_tool']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

        created_by_user = CustomUser.objects.get(id=data['created_by'])

        event_screening = EventScreening.objects.create(
            event_name=data['event_name'],
            event_purpose=data.get('event_purpose', ''),
            location=data['location'],
            start_date=data['start_date'],
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            duration=data['duration'],
            counselor=data['counselor'],
            selected_tool=data['selected_tool'],
            total_users_to_screened=data["total_users"],
            created_by=created_by_user
        )
        logger.info(
            f"Event screening '{event_screening.event_name}' created successfully.")

        from_email = settings.DEFAULT_FROM_EMAIL
        event_details_snippet = (
            f"Event Name: {event_screening.event_name}\n"
            f"Location: {event_screening.location}\n"
            f"Created By: {created_by_user.first_name} {created_by_user.last_name}\n"
        )

        # --- Notify MH Admins (Actionable) ---
        mh_admins = CustomUser.objects.filter(role='mh_admin', is_active=True)
        mh_subject = f"Action Required: New Event Screening Request - {event_screening.event_name}"
        mh_message = (
            f"Dear MH Admin,\n\n"
            f"A new event screening has been requested and requires your approval.\n\n"
            f"{event_details_snippet}\n"
            f"Please log in to the system to review and take action."
        )
        for admin in mh_admins:
            # 1. Trigger Email for MH Admin
            send_mail(mh_subject, mh_message, from_email, [admin.email], fail_silently=False)
            # 2. Trigger Notification for MH Admin
            Notification.objects.create(
                notification_for=admin,
                notification=(
                    f"Action Required: New event '{event_screening.event_name}' by {created_by_user.first_name} "
                    f"needs your approval."
                )
            )

        # --- Notify SUD Admins (Informational) ---
        sud_admins = CustomUser.objects.filter(role='sud_admin', is_active=True)
        sud_subject = f"FYI: New Event Screening Submitted - {event_screening.event_name}"
        sud_message = (
            f"Dear SUD Admin,\n\n"
            f"This is to inform you that a new event screening has been submitted for approval.\n\n"
            f"{event_details_snippet}\n"
            f"You will be notified once an action is taken."
        )
        for admin in sud_admins:
            # 1. Trigger Email for SUD Admin
            send_mail(sud_subject, sud_message, from_email, [admin.email], fail_silently=False)
            # 2. Trigger Notification for SUD Admin
            Notification.objects.create(
                notification_for=admin,
                notification=(
                    f"A new event screening '{event_screening.event_name}' has been submitted for approval "
                    f"by {created_by_user.first_name}."
                )
            )

        return JsonResponse({'success': 'Event screening created and notifications sent successfully'}, status=201)

    except json.JSONDecodeError:
        logger.error("Invalid JSON data in request body")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except CustomUser.DoesNotExist:
        logger.error("Creator user not found.")
        return JsonResponse({'error': 'Creator user not found.'}, status=404)
    except Exception as e:
        logger.exception("An error occurred while creating event screening")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_counselor_info(request, counselor_id):
    try:
        # Get the counselor (user)
        counselor_user = CustomUser.objects.get(id=counselor_id)

        # Get the last event for the counselor
        latest_event = EventScreening.objects.filter(
            created_by=counselor_user).last()

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
            assist_risk_severity = json.loads(
                request.POST.get('assistRiskSeverity', '{}'))
            school_env_data = json.loads(
                request.POST.get('schoolEnvData', '{}'))

            user = CustomUser.objects.get(pk=user_id)

            latest_case_screening = user.case_screenings.order_by(
                '-date').first()
            if not latest_case_screening:
                # Optionally create a new case screening if none exists
                latest_case_screening = CaseScreening.objects.create(
                    user=user, date=timezone.now())

            submission_instance = latest_case_screening.case_based_submissions.first()
            if submission_instance:
                submission_instance.gad_data = gad_data.get('responses', [])
                submission_instance.gad_score = gad_data.get('totalScore')
                submission_instance.gad_interpretation = gad_data.get(
                    'interpretation')
                submission_instance.phq_data = phq_data.get('responses', [])
                submission_instance.phq_score = phq_data.get('totalScore')
                submission_instance.phq_interpretation = phq_data.get(
                    'interpretation')
                submission_instance.ace_data = ace_data.get('responses', [])
                submission_instance.ace_score = ace_data.get('totalScore')
                submission_instance.ace_interpretation = ace_data.get(
                    'interpretation')
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
                substance, _ = CaseSubstance.objects.get_or_create(
                    name=substance_name)
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
        logger.exception(
            f"Error occurred while processing submission: {str(e)}")
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
                "total_users_to_screened": event.total_users_to_screened,
                'users': list(event.users.values('id', 'username', 'email')),
                # Add created_by information
                'created_by': {
                    'id': event.created_by.id,
                    'username': event.created_by.username,
                    'email': event.created_by.email,
                    'first_name': event.created_by.first_name,
                    'last_name': event.created_by.last_name,
                } if event.created_by else None 
            }
            events_list.append(event_data)

        return JsonResponse(events_list, safe=False)


@csrf_exempt
@require_POST
def update_event_screening(request):
    """
    Updates an event's approval status and notifies the original applicant and SUD admins.
    """
    try:
        data = json.loads(request.body)
        event_id = data.get('event_id')
        approval_status = data.get('approval_status')
        rejection_reason = data.get('rejection_reason', '')

        if not all([event_id, approval_status]):
            return JsonResponse({'error': 'event_id and approval_status are required.'}, status=400)
        
        if approval_status not in ['approved', 'rejected']:
            return JsonResponse({'error': 'Invalid approval status value.'}, status=400)

        event = get_object_or_404(EventScreening, pk=event_id)
        
        event.approval_status = approval_status
        event.rejection_reason = rejection_reason if approval_status == 'rejected' else ''
        event.save()

        event_creator = event.created_by
        sud_admins = CustomUser.objects.filter(role='sud_admin', is_active=True)
        
        subject = f"Update on Your Event Screening: {event.event_name}"
        status_text = f"has been {approval_status}"

        if approval_status == 'approved':
            body_details = f"Your event screening request for '{event.event_name}' has been approved.\n\nYou may now proceed with the event."
        else:
            body_details = (
                f"We regret to inform you that your event screening request for '{event.event_name}' has been rejected.\n\n"
                f"Reason for rejection: {rejection_reason}"
            )

        creator_email_body = (
            f"Dear {event_creator.first_name},\n\n"
            f"{body_details}\n\n"
            f"Best regards,\n"
            f"The Admin Team"
        )
        
        # --- Send Email to Creator and SUD Admins ---
        recipient_list = [event_creator.email]
        cc_list = [admin.email for admin in sud_admins]
        
        # 1. Trigger Email for both Creator (To) and SUD Admins (CC)
        email = EmailMessage(
            subject=subject,
            body=creator_email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
            cc=cc_list,
        )
        email.send(fail_silently=False)
        logger.info(f"Sent event status update email to {event_creator.email} with CC to SUD admins.")

        # --- Create In-App Notifications ---
        
        # 2. Trigger Notification for Creator
        Notification.objects.create(
            notification_for=event_creator,
            notification=f"Your event '{event.event_name}' {status_text}."
        )

        # 3. Trigger Notification for SUD Admins
        for admin in sud_admins:
            Notification.objects.create(
                notification_for=admin,
                notification=f"The event '{event.event_name}' submitted by {event_creator.first_name} {status_text}."
            )

        return JsonResponse({'message': 'Event updated and notifications sent successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except EventScreening.DoesNotExist:
        return JsonResponse({'error': 'Event not found.'}, status=404)
    except Exception as e:
        logger.exception("Error occurred while updating event screening")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class EventBasedRecordViewSet(viewsets.ModelViewSet):
    queryset = EventBasedSubmission.objects.all().prefetch_related(
        'user', 'event', 'service_and_treatment', 'referral',
        Prefetch('event_substance_risk_measurements',
                 queryset=EventSubstanceRiskMeasurement.objects.all())
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
        Prefetch('case_substance_risk_measurements',
                 queryset=CaseSubstanceRiskMeasurement.objects.all())
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
