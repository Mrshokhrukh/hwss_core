from access.serializers import CustomUserSerializer


class GyalsungCounselorUserSerializer(CustomUserSerializer):
    def create(self, validated_data):
        return super().create(validated_data)
