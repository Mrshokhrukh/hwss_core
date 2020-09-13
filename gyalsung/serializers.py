from rest_framework import serializers

from access.models import CustomUser
from gyalsung.constants import SCREENING_STATUS_CHOICES
from gyalsung.models import GyalsungAssessment


class GyalsungCounselorUserSerializer(serializers.ModelSerializer):
    active_agency_details = serializers.SerializerMethodField()
    gyalsung_status = serializers.SerializerMethodField()

    def get_active_agency_details(self, obj):
        return {
            "agency_name": obj.active_agency.agency_name if obj.active_agency else None,
            "agency_code": obj.active_agency.agency_code if obj.active_agency else None,
            "agency_parent": (
                obj.active_agency.agency_parent if obj.active_agency else None
            ),
        }

    def get_gyalsung_status(self, obj):
        return (
            "screened"
            if obj.gyalsung_status not in ["registered", ""]
            else obj.gyalsung_status
        )

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


class GyalsungReassessmentUserSerializer(GyalsungCounselorUserSerializer):
    def get_gyalsung_status(self, obj):
        return "pending" if obj.gyalsung_status == "screened" else obj.gyalsung_status


class GyalsungAssessmentSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    counselor_user_details = serializers.SerializerMethodField()
    reassessment_user_details = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        """Return username if user exists, otherwise return identity number."""
        return obj.username

    def get_user_details(self, obj):
        return obj.user_details

    def get_counselor_user_details(self, obj):
        return (
            {
                "username": obj.counselor_user.username,
                "first_name": obj.counselor_user.first_name,
                "last_name": obj.counselor_user.last_name,
            }
            if obj.counselor_user
            else None
        )

    def get_reassessment_user_details(self, obj):
        return (
            {
                "username": obj.reassessment_user.username,
                "first_name": obj.reassessment_user.first_name,
                "last_name": obj.reassessment_user.last_name,
            }
            if obj.reassessment_user
            else None
        )

    class Meta:
        model = GyalsungAssessment
        fields = [
            "id",
            "user",
            "identity_number",
            "username",
            "user_details",
            "gad_data",
            "gad_score",
            "gad_interpretation",
            "phq_data",
            "phq_score",
            "phq_interpretation",
            "ace_data",
            "ace_score",
            "ace_interpretation",
            "psy_data",
            "psy_score",
            "psy_interpretation",
            "submission_date",
            "final_screening_status",
            "is_reassessment_screening",
            "counselor_user",
            "counselor_user_details",
            "reassessment_user",
            "reassessment_user_details",
            "counselor_remarks",
            "reassessment_remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "submission_date",
            "created_at",
            "updated_at",
            "username",
            "user_details",
        ]
