import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserSubmission, TestType, QuestionSet, Submission
from access.models import CustomUser

# Get logger instance
logger = logging.getLogger(__name__)

@csrf_exempt
def save_submission(request):
    if request.method == 'POST':
        # Log the request body
        logger.info('Received POST request with body: %s', request.body)

        # Get the submission data from the request body
        try:
            submission_data = json.loads(request.body)
        except json.JSONDecodeError as e:
            # Log the JSON decoding error
            logger.error('Error decoding JSON: %s', str(e))
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

        # Extract user_id from submission data
        user_id = submission_data[0].get('user')

        if user_id is None:
            # Log the missing user ID error
            logger.error('User ID is required')
            return JsonResponse({'error': 'User ID is required'}, status=400)

        try:
            # Check if the user exists
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            # Log the user does not exist error
            logger.error('User with ID %s does not exist', user_id)
            return JsonResponse({'error': f'User with ID {user_id} does not exist'}, status=400)

        # Get or create UserSubmission instance
        test_type_name = submission_data[0].get('test_type_name')
        user_submission, _ = UserSubmission.objects.get_or_create(user=user, test_type_name=test_type_name)

        # Loop through the submissions and create Submission objects
        for submission in submission_data:
            question_set_name = submission.get('question_set_name')
            question = submission.get('question')
            answer = submission.get('answer')
            diagnosis = submission.get('diagnosis', '')
            substance = submission.get('substance', '')
            specify = submission.get('specify', '')
            score = submission.get('score', None)

            # Get or create TestType instance
            test_type, _ = TestType.objects.get_or_create(name=test_type_name, user_submission=user_submission)

            # Get or create QuestionSet instance
            question_set, _ = QuestionSet.objects.get_or_create(name=question_set_name, test_type=test_type)

            # Create Submission instance
            Submission.objects.create(
                user_submission=user_submission,
                question=question,
                answer=answer,
                diagnosis=diagnosis,
                substance=substance,
                specify=specify,
                score=score,
                question_set=question_set
            )

            # Log successful submission
            logger.info('Submission saved successfully: %s', submission)

        return JsonResponse({'message': 'Submissions saved successfully'}, status=201)

    else:
        # Log the error for non-POST requests
        logger.error('Only POST requests are allowed')
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

