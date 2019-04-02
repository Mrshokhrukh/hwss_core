from datetime import datetime
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import EventScreening

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
        required_fields = ['event_name', 'location', 'start_date', 'end_date', 'duration', 'counselor']
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
            counselor=data['counselor']
        )

        # Convert end_date to datetime.date object
        event_screening.end_date = datetime.strptime(event_screening.end_date, '%Y-%m-%d').date()

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
        events = EventScreening.objects.filter(counselor=counselor_name).order_by('-start_date')

        if not events.exists():
            return JsonResponse({'message': 'Counselor information not available'}, status=200)

        latest_event = events.first()

        counselor_info = {
            'event_name': latest_event.event_name,
            'event_purpose': latest_event.event_purpose,
            'location': latest_event.location,
            'start_date': latest_event.start_date,
            'end_date': latest_event.end_date,
            'duration': latest_event.duration,
            'approval_status': latest_event.approval_status,
            'remarks': latest_event.remarks
        }

        return JsonResponse(counselor_info, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)