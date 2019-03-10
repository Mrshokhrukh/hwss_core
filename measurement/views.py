from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Submission
from access.models import CustomUser

@csrf_exempt
def save_submission(request):
    if request.method == 'POST':
        # Get the submission data from the request body
        submission_data = json.loads(request.body)
        
        # Extract user_id from submission data
        user_id = submission_data.get('userId')

        try:
            # Check if the user exists
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        # Create a new Submission object
        submission = Submission(
            test_type_name=submission_data.get('testTypeName'),
            question_set_name=submission_data.get('questionSetName'),
            question=submission_data.get('question'),
            answer=submission_data.get('answer'),
            diagnosis=submission_data.get('diagnosis'),
            substance=submission_data.get('substance'),
            specify=submission_data.get('specify'),
            score=submission_data.get('score'),
            user=user
        )

        # Save the submission to the database
        submission.save()

        return JsonResponse({'message': 'Submission saved successfully'}, status=201)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
