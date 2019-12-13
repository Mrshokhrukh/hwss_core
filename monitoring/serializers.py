from rest_framework import serializers

from access.models import Agency, CustomUser, UserAgency
from gyalsung_users.models import GyalsungUserProfile
from screening.models import CaseBasedSubmission, CaseSubstanceRiskMeasurement, EventBasedSubmission, EventScreening, EventSubstanceRiskMeasurement
from .models import FinalUserSubmission, Referral, ServiceAndTreatment
from django.contrib.contenttypes.models import ContentType


class FinalUserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalUserSubmission
        fields = [
            'id',
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
            'rescreened',
            'rescreening_count',
            'submission_date',
            'service_and_treatment',
        ]
        read_only_fields = ['submission_date', 'rescreening_count']


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'


class UserAgencySerializer(serializers.ModelSerializer):
    agency = AgencySerializer()

    class Meta:
        model = UserAgency
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    agency_details = UserAgencySerializer()
    active_agency = AgencySerializer()
    user_role_agency = serializers.CharField(
        source='agency_details.user_role_agency', read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'identity_number', 'nationality', 'first_name',
            'middle_name', 'last_name', 'date_of_birth', 'gender', 'email',
            'mob_number', 'father_name', 'mother_name', 'perm_add_village',
            'perm_add_gewog', 'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog',
            'ps_add_dzongkhag', 'is_gyalsung', 'academy_code', 'date_joined',
            'role', 'access_level', 'agency_details', 'active_agency', 'user_role_agency'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_active': {'write_only': True},
        }


class ReferredBySerializer(serializers.ModelSerializer):
    active_agency = AgencySerializer()
    user_role_agency = serializers.CharField(
        source='agency_details.user_role_agency', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name',
            'middle_name', 'last_name', 'email',
            'mob_number', 'active_agency', 'user_role_agency'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_active': {'write_only': True},
        }


class CaseSubstanceRiskMeasurementSerializer(serializers.ModelSerializer):
    substance_name = serializers.CharField(source='substance.name')

    class Meta:
        model = CaseSubstanceRiskMeasurement
        fields = ['substance_name', 'measurement', 'risk_flag', 'total_score']


class EventSubstanceRiskMeasurementSerializer(serializers.ModelSerializer):
    substance_name = serializers.CharField(source='substance.name')

    class Meta:
        model = EventSubstanceRiskMeasurement
        fields = ['substance_name', 'measurement', 'risk_flag', 'total_score']


class FinalUserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalUserSubmission
        fields = '__all__'


class EventScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventScreening
        fields = [
            'id', 'event_name', 'event_purpose', 'location', 'start_date',
            'end_date', 'duration', 'counselor', 'approval_status',
            'remarks', 'rejection_reason', 'registration_lockout_end_time',
            'selected_tool'
        ]


class EventBasedSubmissionSerializer(serializers.ModelSerializer):
    event = EventScreeningSerializer()

    class Meta:
        model = EventBasedSubmission
        fields = [
            'id', 'user', 'event', 'gad_data', 'gad_score',
            'gad_interpretation', 'phq_data', 'phq_score',
            'phq_interpretation', 'ace_data', 'ace_score',
            'ace_interpretation', 'school_env_data', 'submission_date',
            'service_and_treatment', 'referral'
        ]


class CaseBasedSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseBasedSubmission
        fields = '__all__'


class GyalsungUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GyalsungUserProfile
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    referred_to = CustomUserSerializer()
    referred_by = CustomUserSerializer()
    assessment = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = '__all__'

    def get_assessment(self, obj):
        content_type = ContentType.objects.get_for_id(obj.content_type_id)
        model_class = content_type.model_class()
        try:
            assessment_object = model_class.objects.get(id=obj.object_id)
        except model_class.DoesNotExist:
            assessment_object = None

        # Use the appropriate serializer based on the model
        if isinstance(assessment_object, FinalUserSubmission):
            return FinalUserSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, EventBasedSubmission):
            return EventBasedSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, CaseBasedSubmission):
            return CaseBasedSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, GyalsungUserProfile):
            return GyalsungUserProfileSerializer(assessment_object).data
        return None


# Main ServiceAndTreatment Serializer
class ServiceAndTreatmentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    referral_instance = ReferralSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        content_type = ContentType.objects.get_for_id(instance.content_type_id)
        model_class = content_type.model_class()

        try:
            assessment_object = model_class.objects.get(id=instance.object_id)
        except model_class.DoesNotExist:
            assessment_object = None

        if isinstance(assessment_object, FinalUserSubmission):
            assessment_serializer = FinalUserSubmissionSerializer(
                assessment_object)
        elif isinstance(assessment_object, EventBasedSubmission):
            assessment_serializer = EventBasedSubmissionSerializer(
                assessment_object)
        elif isinstance(assessment_object, CaseBasedSubmission):
            assessment_serializer = CaseBasedSubmissionSerializer(
                assessment_object)
        elif isinstance(assessment_object, GyalsungUserProfile):
            assessment_serializer = GyalsungUserProfileSerializer(
                assessment_object)
        else:
            assessment_serializer = None

        if assessment_serializer:
            representation['screening_data'] = assessment_serializer.data
        else:
            representation['screening_data'] = "Data not available"

        # Include substance risk measurements
        if isinstance(assessment_object, CaseBasedSubmission):
            case_substances = CaseSubstanceRiskMeasurement.objects.filter(
                case_submission=assessment_object)
            representation['case_substance_risks'] = CaseSubstanceRiskMeasurementSerializer(
                case_substances, many=True).data
        elif isinstance(assessment_object, EventBasedSubmission):
            event_substances = EventSubstanceRiskMeasurement.objects.filter(
                event_submission=assessment_object)
            representation['event_substance_risks'] = EventSubstanceRiskMeasurementSerializer(
                event_substances, many=True).data

        representation.pop('content_type', None)
        representation.pop('object_id', None)

        return representation

    class Meta:
        model = ServiceAndTreatment
        fields = '__all__'


# Referral Serializer to handle referral_instance
class ReferralSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    referred_to = ReferredBySerializer()
    referred_by = ReferredBySerializer()
    assessment = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = '__all__'

    def get_assessment(self, obj):
        content_type = ContentType.objects.get_for_id(obj.content_type_id)
        model_class = content_type.model_class()
        try:
            assessment_object = model_class.objects.get(id=obj.object_id)
        except model_class.DoesNotExist:
            assessment_object = None

        # Use the appropriate serializer based on the model
        if isinstance(assessment_object, FinalUserSubmission):
            return FinalUserSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, EventBasedSubmission):
            return EventBasedSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, CaseBasedSubmission):
            return CaseBasedSubmissionSerializer(assessment_object).data
        elif isinstance(assessment_object, GyalsungUserProfile):
            return GyalsungUserProfileSerializer(assessment_object).data
        return None
