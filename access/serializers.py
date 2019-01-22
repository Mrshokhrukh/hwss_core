from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Agency


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'is_gyalsung', 'identity_number', 'nationality', 'first_name',
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
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.password = make_password(
            validated_data.get('password', instance.password))
        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)
        instance.save()
        return instance


class AgencySerializer(serializers.ModelSerializer):
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
        # Retrieve 'user' from the context
        user_instance = self.context.get('user', None)

        if user_instance:
            agency = Agency.objects.create(user=user_instance, **validated_data)
            return agency
        else:
            raise serializers.ValidationError("User instance is required for creating an Agency.")

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
