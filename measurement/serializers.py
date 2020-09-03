# serializers.py
from rest_framework import serializers

from access.models import Agency, CustomUser
from measurement.models import (
    Measurement,
    MeasurementAssist,
    Submission,
    TestType,
    UserSubmission,
)


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class MeasurementAssistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementAssist
        fields = "__all__"


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"

    def create(self, validated_data):
        # Create the agency instance
        agency_instance = Agency.objects.create(**validated_data)
        return agency_instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    active_agency = AgencySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "active_agency",
            "ps_add_dzongkhag",
            "academy_code",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = "__all__"


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = "__all__"
