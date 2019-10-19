from rest_framework import serializers
from access.models import CustomUser
from monitoring.models import ServiceAndTreatment, Referral
from .models import EventBasedSubmission, EventScreening, EventSubstanceRiskMeasurement,CaseBasedSubmission, CaseScreening, CaseSubstanceRiskMeasurement

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'middle_name', 'last_name', 
            'identity_number', 'nationality', 'date_of_birth', 'gender', 
            'email', 'mob_number', 'perm_add_village', 'perm_add_gewog', 
            'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog', 
            'ps_add_dzongkhag', 'is_gyalsung', 'academy_code', 'role'
        ]

class ServiceAndTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAndTreatment
        fields = [
            'date', 'assessment_status', 'case_status', 
            'counseling', 'follow_up', 'comments', 'referred'
        ]

class ReferralSerializer(serializers.ModelSerializer):
    referred_by = CustomUserSerializer()
    referred_to = CustomUserSerializer()

    class Meta:
        model = Referral
        fields = ['referred_by', 'referred_to', 'date', 'referral_status', 'referral_remarks']

class EventSubstanceRiskMeasurementSerializer(serializers.ModelSerializer):
    substance = serializers.StringRelatedField()

    class Meta:
        model = EventSubstanceRiskMeasurement
        fields = ['substance', 'measurement', 'risk_flag', 'total_score']

class EventScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventScreening
        fields = ['event_name', 'event_purpose', 'location', 'start_date', 'end_date', 'duration', 'counselor', 'approval_status']

class EventBasedSubmissionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Use the detailed user serializer
    event = EventScreeningSerializer()  # Event details
    event_substance_risk_measurements = EventSubstanceRiskMeasurementSerializer(many=True)  # Substance risks
    service_and_treatment = ServiceAndTreatmentSerializer()
    referral = ReferralSerializer()

    class Meta:
        model = EventBasedSubmission
        fields = [
            'user', 'event', 'gad_score', 'gad_interpretation', 'phq_score', 
            'phq_interpretation', 'ace_score', 'ace_interpretation',
            'school_env_data', 'submission_date', 'service_and_treatment', 
            'referral', 'event_substance_risk_measurements'
        ]


class CaseSubstanceRiskMeasurementSerializer(serializers.ModelSerializer):
    substance = serializers.StringRelatedField()

    class Meta:
        model = CaseSubstanceRiskMeasurement
        fields = ['substance', 'measurement', 'risk_flag', 'total_score']

class CaseScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseScreening
        fields = ['case_name', 'purpose', 'dzongkhag', 'date', 'counselor']

class CaseBasedSubmissionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Use the detailed user serializer
    case = CaseScreeningSerializer()  # Case details
    case_substance_risk_measurements = CaseSubstanceRiskMeasurementSerializer(many=True)  # Substance risks
    service_and_treatment = ServiceAndTreatmentSerializer()
    referral = ReferralSerializer()

    class Meta:
        model = CaseBasedSubmission
        fields = [
            'user', 'case', 'gad_score', 'gad_interpretation', 'phq_score', 
            'phq_interpretation', 'ace_score', 'ace_interpretation', 
            'school_env_data', 'submission_date', 'service_and_treatment', 
            'referral', 'case_substance_risk_measurements'
        ]