from rest_framework import serializers
from .models import FinalUserSubmission

class FinalUserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalUserSubmission
        fields = [
            'user',
            'initial_submission',
            'phq_data',
            'phq_score',
            'phq_interpretation',
            'gad_data',
            'gad_score',
            'gad_interpretation',
            'ace_data',
            'ace_score',
            'ace_interpretation',
            'assist_data',
            'assist_score',
            'assist_interpretation',
            'rescreened',
            'rescreening_count',
            'submission_date',
            'service_and_treatment',
        ]
        read_only_fields = ['submission_date', 'rescreening_count']
