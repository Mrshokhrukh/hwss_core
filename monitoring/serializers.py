from rest_framework import serializers

from access.models import Agency, CustomUser, UserAgency
from gyalsung_users.models import GyalsungUserProfile
from screening.models import CaseBasedSubmission, EventBasedSubmission
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

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'identity_number', 'nationality', 'first_name', 
            'middle_name', 'last_name', 'date_of_birth', 'gender', 'email', 
            'mob_number', 'father_name', 'mother_name', 'perm_add_village', 
            'perm_add_gewog', 'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog', 
            'ps_add_dzongkhag', 'is_gyalsung', 'academy_code', 'date_joined', 
            'role', 'access_level', 'agency_details', 'active_agency'
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

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 
            'middle_name', 'last_name', 'email', 
            'mob_number', 'active_agency'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_active': {'write_only': True},
        }

# Serializers for related models (e.g., FinalUserSubmission, EventBasedSubmission, etc.)
class FinalUserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalUserSubmission
        fields = '__all__'

class EventBasedSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBasedSubmission
        fields = '__all__'

class CaseBasedSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseBasedSubmission
        fields = '__all__'

class GyalsungUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GyalsungUserProfile
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'

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
        
        # Determine which serializer to use based on the model class
        if isinstance(assessment_object, FinalUserSubmission):
            assessment_serializer = FinalUserSubmissionSerializer(assessment_object)
        elif isinstance(assessment_object, EventBasedSubmission):
            assessment_serializer = EventBasedSubmissionSerializer(assessment_object)
        elif isinstance(assessment_object, CaseBasedSubmission):
            assessment_serializer = CaseBasedSubmissionSerializer(assessment_object)
        elif isinstance(assessment_object, GyalsungUserProfile):
            assessment_serializer = GyalsungUserProfileSerializer(assessment_object)
        else:
            assessment_serializer = None

        if assessment_serializer:
            representation['screening_data'] = assessment_serializer.data
        else:
            representation['screening_data'] = "Data not available"

        representation.pop('content_type')
        representation.pop('object_id')

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