from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Agency, UserAgency


class CustomUserSerializer(serializers.ModelSerializer):
    active_agency = 'AgencySerializer'(read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'is_staff', 'is_active', 'is_gyalsung', 'identity_number',
            'nationality', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'gender', 'email', 'mob_number', 'father_name', 'mother_name',
            'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
            'profile_picture', 'active_agency', 'academy_code', 'date_joined',
            'password',  'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
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
        fields = ['id', 'agency_code', 'agency_name']

    def create(self, validated_data):
        # Create the agency instance
        agency_instance = Agency.objects.create(**validated_data)
        return agency_instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class UserAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgency
        fields = '__all__'

    def create(self, validated_data):
        # Create the user-agency instance
        user_agency_instance = UserAgency.objects.create(**validated_data)

        # Update user's active agency if needed
        user_instance = validated_data.get('user')
        agency_instance = validated_data.get('agency')
        if user_instance and agency_instance:
            user_instance.active_agency = agency_instance
            user_instance.save()

        return user_agency_instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Update user's active agency if needed
        user_instance = instance.user
        agency_instance = instance.agency
        if user_instance and agency_instance:
            user_instance.active_agency = agency_instance
            user_instance.save()

        return instance


class PreRecordedUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'is_staff', 'is_active', 'is_gyalsung', 'identity_number',
            'nationality', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'gender', 'email', 'mob_number', 'father_name', 'mother_name',
            'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
            'profile_picture', 'active_agency', 'academy_code', 'date_joined',
            'password',  'role'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance