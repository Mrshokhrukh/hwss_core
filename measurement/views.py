from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import json

from access.models import UserAgency
from .models import ActiveUser, CustomUser, LifetimeUser, MeasurementSubstance, UserSubmission, TestType, QuestionSet, Submission, Measurement, MeasurementAssist
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
from monitoring.models import Rescreening
from django.contrib.auth import get_user_model
from django.db.models import Count

logger = logging.getLogger(__name__)

moderate_threshold = 14


@csrf_exempt
def save_submission(request):
    if request.method == 'POST':
        try:
            submission_data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error('Error decoding JSON: %s', str(e))
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

        user_id = submission_data.get('user')

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

            # Check eligibility for LifetimeUser
            if is_eligible_for_lifetime_user(submission_data):
                register_lifetime_user(user, user_submission, submission_data)
            else:
                normal_saving_process(
                    user, user_submission, submission_data, test_type)

            return JsonResponse({'message': 'Submissions saved successfully'}, status=201)

    else:
        logger.error('Only POST requests are allowed')
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def is_eligible_for_lifetime_user(submission_data):
    all_never_used = all(value['score'] == 0 for key, value in submission_data.items(
    ) if key.endswith('_question_1'))
    return all_never_used


def register_lifetime_user(user, user_submission, submission_data):
    lifetime_user = LifetimeUser.objects.create(
        user=user, user_submission=user_submission)
    for key, value in submission_data.items():
        if key.endswith('_question_1'):
            substance_name = value['substance']
            substance, _ = MeasurementAssist.objects.get_or_create(
                name=substance_name)
            lifetime_user.substances_used.add(substance)
    logger.info('User registered as LifetimeUser')


def normal_saving_process(user, user_submission, submission_data, test_type):
    for key, value in submission_data.items():
        if key.endswith('_question_1'):
            question_set_name = value['question_set_name']
            question_set = None

            for question_key, question_value in submission_data.items():
                if question_key.startswith(question_set_name):
                    question = question_value['question']
                    answer = question_value['answer']
                    score = question_value['score']
                    substance = question_value['substance']
                    specify = question_value['specify']
                    diagnosis = question_value['diagnosis']

                    if question_set is None:
                        question_set, _ = QuestionSet.objects.get_or_create(
                            name=question_set_name, test_type=test_type, user_submission=user_submission)

                    # Create the submission and save scores
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

    measurement_assist, created = MeasurementAssist.objects.get_or_create(
        user=user, user_submission=user_submission
    )

    measurement, created = Measurement.objects.get_or_create(
        user=user, user_submission=user_submission, assist=measurement_assist
    )
    user_submission_instance = exec_measurement(user, user_submission)

    if not LifetimeUser.objects.filter(user=user, user_submission=user_submission).exists():
        active_user = ActiveUser.objects.create(
            user=user, user_submission=user_submission)
        logger.info('User registered as ActiveUser')


def save_rescreening_record(user, user_submission):
    try:
        submission_diagnosis = Submission.objects.get(
            user_submission=user_submission, question_set__name='Diagnosis')
        measurement = Measurement.objects.get(user_submission=user_submission)
        measurement_assist = MeasurementAssist.objects.get(
            user_submission=user_submission)
        Rescreening.objects.create(user=user, submission_diagnosis=submission_diagnosis,
                                   measurement=measurement, measurement_assist=measurement_assist)
        logger.info(
            'Rescreening record saved successfully for user: %s', user.username)
    except ObjectDoesNotExist:
        logger.error(
            'Failed to save rescreening record for user: %s', user.username)


def calculate_score(submission, set_name):
    logger.info('Calculating score for submission %s and set name %s',
                submission.id, set_name)
    scores = [s.score or 0 for s in Submission.objects.filter(
        user_submission=submission.user_submission, question_set__name=set_name)]
    total_score = sum(scores)
    logger.info('Total score calculated: %s', total_score)
    return total_score


def get_flag_color(risk_level):
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
    logger.info('Calculating age for date of birth: %s', date_of_birth)
    today = datetime.date.today()
    age = today.year - date_of_birth.year - \
        ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    logger.info('Calculated age: %s', age)
    return age


def get_substance_score(user, substance):
    logger.info('Retrieving substance score for user: %s, substance: %s',
                user.username, substance)
    submission = Submission.objects.filter(
        user_submission__user=user, substance__iexact=substance).order_by('-created_at').first()

    if submission:
        logger.info('Found submission for substance %s with score: %s',
                    substance, submission.score)
        return int(submission.score) if submission.score is not None else 0
    else:
        logger.warning('No submission found for substance %s', substance)
        return 0


def calculate_phq_measurement_and_flag(user, submission, measurement):
    phq2_score = calculate_score(submission, "PHQ2")
    phq9_score = calculate_score(submission, "PHQ9")
    total_score = phq2_score + phq9_score

    measurement.phq_score = int(total_score)
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


def calculate_gad_measurement_and_flag(user, submission, measurement):
    gad2_score = calculate_score(submission, "GAD2")
    gad7_score = calculate_score(submission, "GAD7")
    total_score = gad2_score + gad7_score

    measurement.gad_score = int(total_score)
    set_measurement_and_flag(measurement, total_score, [(4, "minimal", "green"), (
        9, "mild", "blue"), (14, "moderate", "yellow")], "gad_measurement", "gad_flag")


def calculate_substance_risk(age, substance_scores):
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

        if substance.lower() == 'any drug' and score != 0:
            risk_levels[substance] = 'high risk'
        elif age > 17 and score <= low_risk:
            risk_levels[substance] = 'low risk'
        elif score >= high_risk:
            risk_levels[substance] = 'high risk'
        elif score >= moderate_risk:
            risk_levels[substance] = 'moderate risk'
        else:
            risk_levels[substance] = 'no risk'

    return risk_levels


def update_measurement_assist(user, user_submission, substance_risk_levels):
    measurement_assist, _ = MeasurementAssist.objects.get_or_create(
        user=user,
        user_submission=user_submission
    )
    
    for substance, risk_level in substance_risk_levels.items():
        measurement_field = f'{substance.lower()}_measurement'
        flag_field = f'{substance.lower()}_flag'
        score_field = f'{substance.lower()}_score'

        # Ensure scores are not None, replace with 0 if necessary
        substance_score = get_substance_score(user, substance)
        substance_score = int(substance_score or 0)  # Force integer, handle None
        
        setattr(measurement_assist, measurement_field, risk_level)
        setattr(measurement_assist, flag_field, get_flag_color(risk_level))
        setattr(measurement_assist, score_field, substance_score)  # Save the correct score

    measurement_assist.save()
    logger.info('Measurement assist updated successfully')


@transaction.atomic
def exec_measurement(user, user_submission):
    age = calculate_age(user.date_of_birth)
    submissions = Submission.objects.filter(
        user_submission__user=user).select_related('question_set')

    logger.info('Calculating measurements for user: %s', user.username)
    logger.info('User age: %s', age)

    # Initialize the measurement object for this submission
    measurement, _ = Measurement.objects.get_or_create(
        user=user, user_submission=user_submission)

    for submission in submissions:
        question_set_name = submission.question_set.name

        # Process PHQ submissions and calculate scores
        if question_set_name.startswith("PHQ"):
            calculate_phq_measurement_and_flag(user, submission, measurement)

        # Process GAD submissions and calculate scores
        elif question_set_name.startswith("GAD"):
            calculate_gad_measurement_and_flag(user, submission, measurement)

    measurement.save()

    # Calculate substance risk and update MeasurementAssist
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
    substance_scores = defaultdict(lambda: {'total': 0, 'questions': {}, 'other_name': None})
    null_score_substances = []  # List to store substances with NULL score
    
    submissions = Submission.objects.filter(
        user_submission=user_submission
    ).select_related('question_set')
    
    substance_field_mapping = {
        'tobacco products (cigarettes, chewing tobacco etc)': 'tobacco',
        'alcoholic beverages (beer, wine, spirits, ara etc.)': 'alcoholic',
        'cannabis (marijuana, pot, grass, hash, black etc.)': 'cannabis',
        'cocaine': 'cocaine',
        'amphetamine-type stimulants (meth, ecstasy, yebe, diet pills etc.)': 'amphetamine',
        'inhalants (dendrite, glue, petrol, paint thinner, etc.)': 'inhalants',
        'sedatives or sleeping pills (n-10, diazepam etc.)': 'sedatives',
        'hallucinogens (lsd, trips, ketamine, etc.)': 'hallucinogens',
        'opioids (heroin, morphine, fentanyl, codeine, sp+, tramadol, bs etc.)': 'opioids',
        'other - specify': 'other'
    }
    
    # First pass: Collect all scores and track NULL scores
    for submission in submissions:
        if submission.substance:
            substance_name = submission.substance.strip().lower()
            
            # Track NULL scores
            if submission.score is None:
                null_score_substances.append(submission.substance)
                logger.info(f"Found NULL score for substance: {submission.substance}")
            
            score = submission.score if submission.score is not None else 0
            substance_scores[substance_name]['questions'][submission.question] = score
    
    logger.info('Substances with NULL score: %s', null_score_substances)
    
    # Set other_name based on NULL scores
    other_name = null_score_substances[0] if null_score_substances else None
    logger.info(f"Setting other_name to: {other_name}")
    
    # Calculate total scores
    for substance_name, data in substance_scores.items():
        total_score = sum(data['questions'].values())
        substance_scores[substance_name]['total'] = total_score
        logger.info(f"Total score for {substance_name}: {total_score}")
    
    # Normalize scores for risk calculation
    normalized_scores = {}
    for substance_name, data in substance_scores.items():
        field_name = None
        for original, mapped in substance_field_mapping.items():
            if substance_name == original.lower():
                field_name = mapped
                break
        if field_name:
            normalized_scores[field_name.capitalize()] = data['total']
    
    substance_risk_levels = calculate_substance_risk(age, normalized_scores)
    logger.info('Calculated risk levels: %s', substance_risk_levels)
    
    # Create or update MeasurementAssist
    measurement_assist, created = MeasurementAssist.objects.get_or_create(
        user=user,
        user_submission=user_submission
    )
    
    # Set the other_name field
    measurement_assist.other_name = other_name
    logger.info(f"Set measurement_assist.other_name to: {other_name}")
    
    # Update measurements, flags, and scores
    for substance, risk_level in substance_risk_levels.items():
        field_base = substance.lower()
        
        original_substance = None
        for substance_name, data in substance_scores.items():
            mapped_field = None
            for original, mapped in substance_field_mapping.items():
                if substance_name == original.lower():
                    mapped_field = mapped
                    break
            if mapped_field and mapped_field.capitalize() == substance:
                original_substance = substance_name
                break

        # Set measurement
        measurement_field = f'{field_base}_measurement'
        if hasattr(measurement_assist, measurement_field):
            setattr(measurement_assist, measurement_field, risk_level)
            logger.info(f"Set {measurement_field} to {risk_level}")

        # Set flag
        flag_field = f'{field_base}_flag'
        if hasattr(measurement_assist, flag_field):
            flag_color = get_flag_color(risk_level)
            setattr(measurement_assist, flag_field, flag_color)
            logger.info(f"Set {flag_field} to {flag_color}")

        # Set score
        score_field = f'{field_base}_score'
        if hasattr(measurement_assist, score_field):
            total_score = substance_scores.get(original_substance, {'total': 0})['total']
            setattr(measurement_assist, score_field, total_score)
            logger.info(f"Set {score_field} to {total_score}")
    
    # Handle injection risk
    any_drug_score = substance_scores.get('any drug', {'total': 0})['total']
    if any_drug_score > 0:
        measurement_assist.injection_measurement = 'high risk'
        measurement_assist.injection_flag = 'red'
        measurement_assist.injection_score = any_drug_score
        logger.info(f"Set injection_measurement to high risk and injection_score to {any_drug_score}")
    else:
        measurement_assist.injection_measurement = 'no risk'
        measurement_assist.injection_flag = 'green'
        measurement_assist.injection_score = 0
        logger.info("Set injection_measurement to no risk and injection_score to 0")
    
    # Save changes
    try:
        measurement_assist.save()
        logger.info('Measurement assist saved successfully')
    except Exception as e:
        logger.error(f"Failed to save measurement assist: {e}")


class MeasurementListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def list(self, request, *args, **kwargs):
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
        measurement_assists = MeasurementAssistSerializer(
            queryset, many=True).data

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


class CombinedListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # Default return method with user details
        return self.get_default_format()

    def get_default_format(self):
        # Fetch queryset based on serializer class
        queryset = self.filter_queryset(self.get_queryset())

        if queryset is None:
            return Response([])  # Return empty response if queryset is None

        # Determine serializer class
        serializer_class = self.get_serializer_class()

        # Fetch all data
        data = serializer_class(queryset, many=True).data

        # Include custom user details
        user_ids = queryset.values_list('user_id', flat=True).distinct()
        users = CustomUser.objects.filter(id__in=user_ids)
        user_details = CustomUserSerializer(users, many=True).data

        # Pair each data with its respective user
        paired_data = []
        for item, user_detail in zip(data, user_details):
            paired_data.append({
                self.item_name: item,
                'user_details': user_detail
            })

        return Response(paired_data)

    def get_queryset(self):
        # Define queryset based on view name
        if 'measurement' in self.kwargs.get('view_name', ''):
            return Measurement.objects.all()
        elif 'assist' in self.kwargs.get('view_name', ''):
            return MeasurementAssist.objects.all()
        else:
            return None

    def get_serializer_class(self):
        # Define serializer class based on view name
        if 'measurement' in self.kwargs.get('view_name', ''):
            return MeasurementSerializer
        elif 'assist' in self.kwargs.get('view_name', ''):
            return MeasurementAssistSerializer
        else:
            return None

    @property
    def item_name(self):
        if 'measurement' in self.kwargs.get('view_name', ''):
            return 'measurement'
        elif 'assist' in self.kwargs.get('view_name', ''):
            return 'measurement_assist'
        else:
            return 'item'


def check_and_save_lifetime_user(request):
    users = CustomUser.objects.all()
    for user in users:
        submissions = Submission.objects.filter(
            user_submission__user=user,
            question_set__name='ASSIST',
            question='In the past three months, how often have you used?',
            score=0
        )

        if submissions.exists():
            user_submission, created = UserSubmission.objects.get_or_create(
                user=user)

            lifetime_user, created = LifetimeUser.objects.get_or_create(
                user=user, user_submission=user_submission)

            for submission in submissions:
                for substance_name in submission.substance.split(', '):
                    substance, created = MeasurementSubstance.objects.get_or_create(
                        name=substance_name)
                    if created:
                        substance.save()
                    lifetime_user.substances_used.add(substance)

            # Save the LifetimeUser instance
            lifetime_user.save()

    return JsonResponse({'message': 'Lifetime users created successfully'})


def get_lifetime_and_active_users(request):
    lifetime_users = LifetimeUser.objects.all()
    active_users = ActiveUser.objects.all()
    CustomUser = get_user_model()

    lifetime_users_data = [{'user_id': user.user_id, 'username': user.user.username,
                            'full_name': f"{user.user.first_name} {user.user.last_name}",
                            'age': calculate_age(user.user.date_of_birth),
                            'sex': user.user.gender,
                            'ps_dzongkhag': user.user.ps_add_dzongkhag,
                            'cid': user.user.identity_number,
                            'substances_used': [substance.name for substance in user.substances_used.all()]}
                           for user in lifetime_users]

    active_users_data = [{'user_id': user.user_id, 'username': user.user.username,
                          'full_name': f"{user.user.first_name} {user.user.last_name}",
                          'age': calculate_age(user.user.date_of_birth),
                          'sex': user.user.gender,
                          'ps_dzongkhag': user.user.ps_add_dzongkhag,
                          'cid': user.user.identity_number,
                          'substances_used': [substance.name for substance in user.substances_used.all()]}
                         for user in active_users]

    response_data = {
        'lifetime_users': lifetime_users_data,
        'active_users': active_users_data
    }

    return JsonResponse(response_data, safe=False)


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def main_composer(request):
    users = CustomUser.objects.all()
    for user in users:
        check_and_save_lifetime_user(request)
    response = get_lifetime_and_active_users(request)

    return response


@csrf_exempt
def fetch_school_env_entries(request):
    if request.method == 'GET':
        submissions = Submission.objects.filter(
            question_set__name="SCHOOL ENV")
        data = {}
        for submission in submissions:
            user = submission.user_submission.user

            user_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "gender": user.gender,
                "perm_add_village": user.perm_add_village,
                "perm_add_gewog": user.perm_add_gewog,
                "perm_add_dzongkhag": user.perm_add_dzongkhag,
                "ps_add_village": user.ps_add_village,
                "ps_add_gewog": user.ps_add_gewog,
                "ps_add_dzongkhag": user.ps_add_dzongkhag,
                "role": user.get_role_display(),
            }

            # Include active agency details
            if user.active_agency:
                user_data["active_agency"] = {
                    "agency_code": user.active_agency.agency_code,
                    "agency_name": user.active_agency.agency_name,
                }

            # Include UserAgency details if available
            try:
                user_agency = user.agency_details
                user_data["user_agency"] = {
                    "agency_name": user_agency.agency.agency_name,
                    "user_code": user_agency.user_code,
                    "parent_occupation": user_agency.parent_occupation,
                    "guardian_name": user_agency.guardian_name,
                    "guardian_occupation": user_agency.guardian_occupation,
                    "parent_status": user_agency.parent_status,
                    "current_living_with": user_agency.current_living_with,
                    "user_role_agency": user_agency.user_role_agency,
                    "user_class": user_agency.user_class,
                    "user_stream": user_agency.user_stream,
                    "user_sub_class": user_agency.user_sub_class,
                }
            except UserAgency.DoesNotExist:
                user_data["user_agency"] = None

            # Add user data to the response
            if user.username not in data:
                data[user.username] = {
                    "user_details": user_data,
                    "submissions": [],
                }

            # Append submission details
            data[user.username]["submissions"].append({
                "question": submission.question,
                "answer": submission.answer,
                "score": submission.score,
                "substance": submission.substance,
                "specify": submission.specify,
                "diagnosis": submission.diagnosis,
                "created_at": submission.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
