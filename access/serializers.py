from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Agency


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'is_gyalsung', 'identity_number', 'nationality', 'first_name',
            'middle_name', 'last_name', 'date_of_birth', 'gender', 'email', 'mob_number',
            'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = [
            'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag',
            'father_name', 'mother_name', 'parent_occupation', 'guardian_name',
            'guardian_occupation', 'parent_status', 'current_living_with',
            'agency_code', 'user_role_agency', 'agency_name', 'user_class',
            'user_sub_class', 'academy_code', 'status',
        ]

    def create(self, validated_data):
        # Get the user instance from the context
        user_instance = self.context.get('user_instance')

        # Ensure that the user instance is provided
        if not user_instance:
            raise ValueError("User instance is required to create an agency")

        # Create the agency instance with the user_instance
        agency_instance = Agency.objects.create(user=user_instance, **validated_data)
        return agency_instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

class PreRecordedAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = [
            'user_code', 'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag',
            'father_name', 'mother_name', 'parent_occupation', 'guardian_name',
            'guardian_occupation', 'parent_status', 'current_living_with',
            'agency_code', 'user_role_agency', 'agency_name', 'user_class',
            'user_sub_class', 'academy_code', 'status',
        ]

    def create(self, validated_data):
        # Retrieve 'user_id' from the context
        user_id = self.context.get('user_id')

        if user_id:
            try:
                # Fetch the user instance based on the user ID
                user_instance = CustomUser.objects.get(id=user_id)

                # Set the 'user' field with the correct user instance
                validated_data['user'] = user_instance

                # Create the Agency instance
                agency = Agency.objects.create(**validated_data)
                return agency
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
        else:
            raise serializers.ValidationError(
                "User ID is required for creating an Agency.")

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
