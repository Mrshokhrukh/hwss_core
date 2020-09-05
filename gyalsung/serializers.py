from rest_framework import serializers
from access.models import CustomUser
from .models import GyalsungAssessment
from  .constants import SCREENING_STATUS_CHOICES

class GyalsungCounselorUserSerializer(serializers.ModelSerializer):
    active_agency_details = serializers.SerializerMethodField()

    def get_active_agency_details(self, obj):
        return {
            "agency_name": obj.active_agency.agency_name if obj.active_agency else None,
            "agency_code": obj.active_agency.agency_code if obj.active_agency else None,
            "agency_parent": (
                obj.active_agency.agency_parent if obj.active_agency else None
            ),
        }

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "is_gyalsung",
            "identity_number",
            "nationality",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "email",
            "mob_number",
            "father_name",
            "mother_name",
            "perm_add_village",
            "perm_add_gewog",
            "perm_add_dzongkhag",
            "profile_picture",
            "academy_code",
            "date_joined",
            "role",
            "active_agency",
            "active_agency_details",
            "gyalsung_status",
            "guard_mob_number",
            "hospital_name",
            "hospital_dzongkhag",
            "appointment_date",
            "academy_name",
            "personal_number",
            "registration_method",
        ]


class GyalsungAssessmentSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    counselor_user_details = serializers.SerializerMethodField()
    reassessment_user_details = serializers.SerializerMethodField()

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "email": obj.user.email,
        } if obj.user else None

    def get_counselor_user_details(self, obj):
        return {
            "username": obj.counselor_user.username,
            "first_name": obj.counselor_user.first_name,
            "last_name": obj.counselor_user.last_name,
        } if obj.counselor_user else None

    def get_reassessment_user_details(self, obj):
        return {
            "username": obj.reassessment_user.username,
            "first_name": obj.reassessment_user.first_name,
            "last_name": obj.reassessment_user.last_name,
        } if obj.reassessment_user else None

    class Meta:
        model = GyalsungAssessment
        fields = [
            'id', 'user', 'user_details', 'gad_data', 'gad_score', 'gad_interpretation',
            'phq_data', 'phq_score', 'phq_interpretation', 'ace_data',
            'ace_score', 'ace_interpretation', 'psy_data', 'psy_score',
            'psy_interpretation', 'submission_date', 'final_screening_status',
            'is_reassessment_screening', 'counselor_user', 'counselor_user_details',
            'reassessment_user', 'reassessment_user_details', 'counselor_remarks',
            'reassessment_remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'submission_date', 'created_at', 'updated_at']

    def validate_final_screening_status(self, value):
        """Validate that the screening status is a valid choice"""
        if value and value not in dict(SCREENING_STATUS_CHOICES).keys():
            raise serializers.ValidationError(
                f"'{value}' is not a valid choice. Valid choices are: {list(dict(SCREENING_STATUS_CHOICES).keys())}"
            )
        return value

    def validate_counselor_user(self, value):
        """Validate that counselor_user exists"""
        if value and not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Counselor user does not exist")
        return value

    def validate_reassessment_user(self, value):
        """Validate that reassessment_user exists"""
        if value and not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Reassessment user does not exist")
        return value

    def validate_user(self, value):
        """Validate that user exists"""
        if value and not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist")
        return value