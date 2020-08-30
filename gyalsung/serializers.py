from access.models import CustomUser
from rest_framework import serializers


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
            "is_staff",
            "is_active",
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
            "registration_method",
        ]
