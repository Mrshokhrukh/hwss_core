from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
import json
from .models import CustomUser, UserSubmission, TestType, QuestionSet, Submission, Measurement, MeasurementAssist
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import ObjectDoesNotExist
import logging
import re
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
from rest_framework import generics
from .serializers import CustomUserSerializer, MeasurementSerializer, MeasurementAssistSerializer, SubmissionSerializer, TestTypeSerializer, UserSubmissionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, permissions

from django.db.models import Count

logger = logging.getLogger(__name__)


@csrf_exempt
def save_submission(request):
    if request.method == 'POST':
        try:
            logger.info('Received submission data: %s', request.body)
            submission_data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error('Error decoding JSON: %s', str(e))
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

        user_id = submission_data.get('user')
        logger.debug('Extracted user ID: %s', user_id)

        if user_id is None:
            logger.error('User ID is required')
            return JsonResponse({'error': 'User ID is required'}, status=400)

        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            logger.error('User with ID %s does not exist', user_id)
            return JsonResponse({'error': f'User with ID {user_id} does not exist'}, status=400)

        test_type_name = submission_data.get('test_type_name')
        test_type, _ = TestType.objects.get_or_create(name=test_type_name)

        with transaction.atomic():
            existing_submissions = UserSubmission.objects.filter(
                user=user, test_type=test_type)

            if existing_submissions.exists():
                if submission_data.get('confirmation'):
                    logger.info(
                        'User %s confirmed submission for test type %s again', user_id, test_type_name)
                    # Remove existing submissions for the same test type
                    existing_submissions.delete()
                else:
                    logger.warning(
                        'User %s has already submitted for test type %s', user_id, test_type_name)
                    return JsonResponse({'error': f'User {user_id} has already submitted for test type {test_type_name}'}, status=400)

            user_submission, created = UserSubmission.objects.get_or_create(
                user=user, test_type=test_type)

            if not created:
                logger.warning(
                    'User %s has already submitted for test type %s', user_id, test_type_name)
                return JsonResponse({'error': f'User {user_id} has already submitted for test type {test_type_name}'}, status=400)

            for key, value in submission_data.items():
                # Check if the key represents a question
                if key.endswith('_question_1'):
                    question_set_name = value['question_set_name']
                    question_set = None

                    # Iterate through all questions in the submission data
                    for question_key, question_value in submission_data.items():
                        if question_key.startswith(question_set_name):
                            question = question_value['question']
                            answer = question_value['answer']
                            score = question_value['score']
                            substance = question_value['substance']
                            specify = question_value['specify']
                            diagnosis = question_value['diagnosis']

                            # Create or get the question set
                            if question_set is None:
                                question_set, _ = QuestionSet.objects.get_or_create(
                                    name=question_set_name, test_type=test_type, user_submission=user_submission)

                            # Create the submission for each question in the set
                            Submission.objects.create(
                                user_submission=user_submission,
                                question=question,
                                answer=answer,
                                score=score,
                                substance=substance,
                                specify=specify,
                                diagnosis=diagnosis,
                                question_set=question_set
                            )

            logger.info('Submissions saved successfully')
            # Pass user_submission object to exec_measurement
            exec_measurement(user, user_submission)
            return JsonResponse({'message': 'Submissions saved successfully'}, status=201)

    else:
        logger.error('Only POST requests are allowed')
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def calculate_score(submission, set_name):
    """
    Calculate the total score for the given submission and set name.
    """
    logger.info('Calculating score for submission %s and set name %s',
                submission.id, set_name)
    scores = [s.score or 0 for s in Submission.objects.filter(
        user_submission=submission.user_submission, question_set__name=set_name)]
    total_score = sum(scores)
    logger.info('Total score calculated: %s', total_score)
    return total_score


def get_flag_color(risk_level):
    """
    Get the flag color based on the risk level.
    """
    logger.info('Getting flag color for risk level: %s', risk_level)
    if risk_level == 'high risk':
        flag_color = 'red'
    elif risk_level == 'moderate risk':
        flag_color = 'yellow'
    elif risk_level == 'low risk':
        flag_color = 'blue'
    else:
        flag_color = ''
    logger.info('Flag color retrieved: %s', flag_color)
    return flag_color


def set_measurement_and_flag(measurement, total_score, thresholds, measurement_field, flag_field):
    """
    Set measurement and flag based on total score and thresholds.
    """
    logger.info('Setting measurement and flag for total score: %s', total_score)
    for threshold, measurement_value, flag_value in thresholds:
        if total_score <= threshold:
            logger.info('Setting measurement: %s, flag: %s',
                        measurement_value, flag_value)
            setattr(measurement, measurement_field, measurement_value)
            setattr(measurement, flag_field, flag_value)
            break
    else:
        # Set defaults if score exceeds all thresholds
        logger.warning('Score exceeds all thresholds, setting defaults')
        setattr(measurement, measurement_field, "severe")
        setattr(measurement, flag_field, "red")


def calculate_age(date_of_birth):
    """
    Calculate the age of the user based on the date of birth.
    """
    logger.info('Calculating age for date of birth: %s', date_of_birth)
    today = datetime.date.today()
    age = today.year - date_of_birth.year - \
        ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    logger.info('Calculated age: %s', age)
    return age


def get_substance_score(user, substance):
    """
    Retrieve the substance score for the given user and substance.
    """
    logger.info('Retrieving substance score for user: %s, substance: %s',
                user.username, substance)
    # Retrieve the most recent submission for the user and substance
    submission = Submission.objects.filter(
        user_submission__user=user, substance=substance).order_by('-created_at').first()

    if submission:
        logger.info('Found submission for substance %s with score: %s',
                    substance, submission.score)
        return submission.score if submission.score is not None else 0
    else:
        logger.warning('No submission found for substance %s', substance)
        return 0


def calculate_phq_measurement_and_flag(user, submission, measurement):
    """
    Calculate PHQ measurement and flag for the given submission and user.
    """
    phq2_score = calculate_score(submission, "PHQ2")
    phq9_score = calculate_score(submission, "PHQ9")
    total_score = phq2_score + phq9_score

    logger.info('PHQ2 Score: %s', phq2_score)
    logger.info('PHQ9 Score: %s', phq9_score)
    logger.info('Total Score: %s', total_score)

    set_measurement_and_flag(measurement, total_score, [(4, "minimal", "green"), (9, "mild", "blue"), (
        14, "moderate", "yellow"), (19, "moderately severe", "orange")], "phq_measurement", "phq_flag")

    suicidal_question = Submission.objects.filter(user_submission=submission.user_submission, question_set__name="PHQ9",
                                                  question__icontains="Thoughts that you would be better off dead, or of hurting yourself").first()
    if suicidal_question and suicidal_question.score is not None:
        logger.info('Suicidal Question Score: %s', suicidal_question.score)
        if suicidal_question.score == 1:
            measurement.suicidal_measurement = "several days"
            measurement.suicidal_flag = "yellow"
        elif suicidal_question.score == 2:
            measurement.suicidal_measurement = "more than half the days"
            measurement.suicidal_flag = "orange"
        elif suicidal_question.score == 3:
            measurement.suicidal_measurement = "nearly everyday"
            measurement.suicidal_flag = "red"
    else:
        logger.info('No Suicidal Question or Score found')

    logger.info('PHQ Measurement: %s', measurement.phq_measurement)
    logger.info('PHQ Flag: %s', measurement.phq_flag)


def calculate_gad_measurement_and_flag(user, submission, measurement):
    """
    Calculate GAD measurement and flag for the given submission and user.
    """
    gad2_score = calculate_score(submission, "GAD2")
    gad7_score = calculate_score(submission, "GAD7")
    total_score = gad2_score + gad7_score

    logger.info('GAD2 Score: %s', gad2_score)
    logger.info('GAD7 Score: %s', gad7_score)
    logger.info('Total GAD Score: %s', total_score)

    set_measurement_and_flag(measurement, total_score, [(4, "minimal", "green"), (
        9, "mild", "blue"), (14, "moderate", "yellow")], "gad_measurement", "gad_flag")


def calculate_substance_risk(age, substance_scores):
    """
    Calculate the risk levels for substances based on the user's age group and substance scores.
    """
    # Define thresholds based on age
    if age <= 14:
        thresholds = {
            'Tobacco': (0, 3, 27),
            'Alcoholic': (0, 10, 27),
            'Cannabis': (0, 3, 27),
            'Cocaine': (0, 3, 27),
            'Amphetamine': (0, 3, 27),
            'Inhalants': (0, 3, 27),
            'Sedatives': (0, 3, 27),
            'Hallucinogens': (0, 3, 27),
            'Opioids': (0, 3, 27),
            'Other': (0, 3, 27)
        }  # Define thresholds for age group <= 14
    elif 15 <= age <= 17:
        thresholds = {
            'Tobacco': (2, 11, 12),
            'Alcoholic': (5, 17, 18),
            'Cannabis': (2, 11, 12),
            'Cocaine': (2, 6, 7),
            'Amphetamine': (2, 8, 9),
            'Inhalants': (2, 8, 9),
            'Sedatives': (2, 6, 7),
            'Hallucinogens': (2, 8, 9),
            'Opioids': (2, 6, 7),
            'Other': (2, 6, 7)
        }  # Define thresholds for age group 15-17
    else:
        thresholds = {
            'Tobacco': (0, 3, 27),
            'Alcoholic': (0, 10, 27),
            'Cannabis': (0, 3, 27),
            'Cocaine': (0, 3, 27),
            'Amphetamine': (0, 3, 27),
            'Inhalants': (0, 3, 27),
            'Sedatives': (0, 3, 27),
            'Hallucinogens': (0, 3, 27),
            'Opioids': (0, 3, 27),
            'Other': (0, 3, 27)
        }  # Define thresholds for age group > 17

    risk_levels = {}
    for substance, (low_risk, moderate_risk, high_risk) in thresholds.items():
        pattern = re.compile(
            r'\b' + re.escape(substance) + r'\b', re.IGNORECASE)
        matched_substances = [
            s for s in substance_scores.keys() if re.search(pattern, s)]
        score = max([substance_scores[s]
                    for s in matched_substances], default=0)

        if age > 17 and score <= low_risk:
            risk_levels[substance] = 'low risk'
        elif score >= high_risk:
            risk_levels[substance] = 'high risk'
        elif score >= moderate_risk:
            risk_levels[substance] = 'moderate risk'
        else:
            risk_levels[substance] = 'no risk'

    return risk_levels


def update_measurement_assist(user, substance_risk_levels):
    """
    Update the measurement assist object based on substance risk levels.
    """
    logger.info('Updating measurement assist for user: %s', user.username)
    measurement_assist, created = MeasurementAssist.objects.get_or_create(
        user=user)
    for substance, risk_level in substance_risk_levels.items():
        measurement_field = f'{substance.lower()}_measurement'
        flag_field = f'{substance.lower()}_flag'
        logger.info('Updating %s measurement to: %s', substance, risk_level)
        logger.info('Updating %s flag to: %s', substance,
                    get_flag_color(risk_level))
        setattr(measurement_assist, measurement_field, risk_level)
        setattr(measurement_assist, flag_field, get_flag_color(risk_level))
    measurement_assist.save()
    logger.info('Measurement assist updated successfully')


@transaction.atomic
def exec_measurement(user, user_submission):
    age = calculate_age(user.date_of_birth)
    submissions = Submission.objects.filter(
        user_submission__user=user).select_related('question_set')

    logger.info('Calculating measurements for user: %s', user.username)
    logger.info('User age: %s', age)

    for submission in submissions:
        logger.info('Processing submission for question set: %s',
                    submission.question_set.name)
        logger.info('Submission score: %s', submission.score)

        question_set_name = submission.question_set.name

        if question_set_name.startswith("PHQ"):
            process_phq_submission(user, submission)

        elif question_set_name.startswith("GAD"):
            process_gad_submission(user, submission)

    process_substance_measurement(user, age, user_submission)


def process_phq_submission(user, submission):
    phq_score = calculate_score(
        submission, "PHQ2") if submission.question_set.name == "PHQ2" else None
    if phq_score is not None:
        measurement, created = Measurement.objects.get_or_create(
            user=user,
            user_submission=submission.user_submission
        )
        if created or phq_score < 3:
            measurement.phq_measurement = "minimal"
            measurement.phq_flag = "green"
            logger.info(
                'PHQ2 score below threshold, setting minimal measurement and green flag')
        else:
            calculate_phq_measurement_and_flag(user, submission, measurement)
        measurement.save()


def process_gad_submission(user, submission):
    gad_score = calculate_score(
        submission, "GAD2") if submission.question_set.name == "GAD2" else None
    if gad_score is not None:
        measurement = Measurement.objects.filter(
            user=user,
            user_submission=submission.user_submission
        ).first()
        if measurement:
            if gad_score < 3:
                measurement.gad_measurement = "minimal"
                measurement.gad_flag = "green"
                logger.info(
                    'GAD2 score below threshold, updating existing measurement with minimal measurement and green flag')
            else:
                calculate_gad_measurement_and_flag(
                    user, submission, measurement)
            measurement.save()
        else:
            logger.error('No existing measurement found for user submission')


@transaction.atomic
def process_substance_measurement(user, age, user_submission):
    substance_scores = defaultdict(list)
    null_score_substances = []  # List to store substances with NULL score

    submissions = Submission.objects.filter(
        user_submission__user=user).select_related('question_set')
    for submission in submissions:
        if submission.substance:
            substance_scores[submission.substance].append(submission.score)
            if submission.score is None:
                # Add substance with NULL score to the list
                null_score_substances.append(submission.substance)

    repeated_substances = {substance: scores for substance,
                           scores in substance_scores.items() if len(scores) > 1}

    substance_scores = {substance: sum(
        scores) for substance, scores in repeated_substances.items()}

    logger.info('Substance scores for user: %s', substance_scores)

    if null_score_substances:  # Check if there are substances with NULL score
        # Update other_name field with the name of the first substance with NULL score
        other_name = null_score_substances[0]
    else:
        other_name = None  # If no NULL score substances, set other_name to None

    # Print substances with NULL score
    logger.info('Substances with NULL score: %s', null_score_substances)

    substance_risk_levels = calculate_substance_risk(age, substance_scores)
    logger.info('Substance risk levels: %s', substance_risk_levels)

    measurement_assist, created = MeasurementAssist.objects.get_or_create(
        user=user,
        user_submission=user_submission
    )

    measurement_assist.other_name = other_name  # Update other_name field
    measurement_assist.save()

    if created:
        for substance, risk_level in substance_risk_levels.items():
            setattr(measurement_assist,
                    f'{substance.lower()}_measurement', risk_level)
            setattr(measurement_assist,
                    f'{substance.lower()}_flag', get_flag_color(risk_level))
        measurement_assist.save()

        logger.info('Measurement assist updated successfully')

    else:
        for substance, risk_level in substance_risk_levels.items():
            setattr(measurement_assist,
                    f'{substance.lower()}_measurement', risk_level)
            setattr(measurement_assist,
                    f'{substance.lower()}_flag', get_flag_color(risk_level))
        measurement_assist.save()

        logger.info(
            'Measurement assist updated and old record overridden successfully')


class MeasurementListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def list(self, request, *args, **kwargs):
        # Default return method with user details
        return self.get_default_format()

    def get_default_format(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Fetch all measurements
        measurements = MeasurementSerializer(queryset, many=True).data

        # Include custom user details
        user_ids = queryset.values_list('user_id', flat=True).distinct()
        users = CustomUser.objects.filter(id__in=user_ids)
        user_details = CustomUserSerializer(users, many=True).data

        # Pair each measurement with its respective user
        paired_data = []
        for measurement, user_detail in zip(measurements, user_details):
            paired_data.append({
                'measurement': measurement,
                'user_details': user_detail
            })

        return Response(paired_data)


class MeasurementAssistListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MeasurementAssist.objects.all()
    serializer_class = MeasurementAssistSerializer

    def list(self, request, *args, **kwargs):
        # Default return method with user details
        return self.get_default_format()

    def get_default_format(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Fetch all measurement assists
        measurement_assists = MeasurementAssistSerializer(queryset, many=True).data

        # Include custom user details
        user_ids = queryset.values_list('user_id', flat=True).distinct()
        users = CustomUser.objects.filter(id__in=user_ids)
        user_details = CustomUserSerializer(users, many=True).data

        # Pair each measurement assist with its respective user
        paired_data = []
        for assist, user_detail in zip(measurement_assists, user_details):
            paired_data.append({
                'measurement_assist': assist,
                'user_details': user_detail
            })

        return Response(paired_data)


class SubmissionListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Submission.objects.all()

    def list(self, request, *args, **kwargs):
        # Fetch query parameters from the request
        user_id = self.request.query_params.get('user_id')
        user_submission_id = self.request.query_params.get(
            'user_submission_id')

        # If parameters are provided, return submissions based on the parameters
        if user_id or user_submission_id:
            return self.get_filtered_submissions(user_id, user_submission_id)
        else:
            # If no parameters are provided, return the default format with user details
            return self.get_default_format()

    def get_filtered_submissions(self, user_id, user_submission_id):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply filters if provided in the request
        if user_id:
            queryset = queryset.filter(user_submission__user_id=user_id)
        if user_submission_id:
            queryset = queryset.filter(user_submission_id=user_submission_id)

        # Serialize the queryset
        serializer = SubmissionSerializer(queryset, many=True)

        # Fetch user IDs from user_submissions
        user_submission_ids = queryset.values_list(
            'user_submission__user_id', flat=True).distinct()

        # Filter CustomUser queryset based on user IDs from user_submissions
        users = CustomUser.objects.filter(id__in=user_submission_ids)
        user_details = CustomUserSerializer(users, many=True).data

        # Combine submissions and user details into a single dictionary
        data = {
            'user_details': user_details,
            'submissions': serializer.data,
        }

        return Response(data)

    def get_default_format(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Fetch all test types
        test_types = TestTypeSerializer(TestType.objects.all(), many=True).data

        # Fetch all user submissions
        user_submissions = UserSubmissionSerializer(
            UserSubmission.objects.all(), many=True).data

        # Include custom user details
        user_submission_ids = UserSubmission.objects.values_list(
            'user_id', flat=True).distinct()
        users = CustomUser.objects.filter(id__in=user_submission_ids)
        user_details = CustomUserSerializer(users, many=True).data

        # Group submissions by user_submission
        submissions = {}
        for submission in queryset:
            user_submission_id = submission.user_submission_id
            if user_submission_id not in submissions:
                submissions[user_submission_id] = []
            submissions[user_submission_id].append(
                SubmissionSerializer(submission).data)

        # Combine all data into a single dictionary
        data = {
            'test_types': test_types,
            'user_submissions': user_submissions,
            'user_details': user_details,  # Include user details
            'submissions': submissions,
        }

        return Response(data)
