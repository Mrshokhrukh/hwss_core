from access.models import CustomUser
from access.serializers import CustomUserSerializer


class GyalsungCounselorUserSerializer(CustomUserSerializer):

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
            "password",
            "role",
            "active_agency",
            "agency_details",
            "gyalsung_status",
            "registration_method",
        ]
        extra_kwargs = {
            "password": {"read_only": True},
        }
