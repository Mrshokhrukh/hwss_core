# serializers.py
from rest_framework import serializers

from access.models import CustomUser
from .models import Measurement, MeasurementAssist, QuestionSet, Submission, TestType, UserSubmission


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class MeasurementAssistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementAssist
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'active_agency', 'ps_add_dzongkhag', 'academy_code')

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = '__all__'

class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = '__all__'
