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
        # Create a new CustomUser object with the validated data
        user = CustomUser(
            is_gyalsung=validated_data.get('is_gyalsung', False),
            identity_number=validated_data['identity_number'],
            nationality=validated_data['nationality'],
            first_name=validated_data['first_name'],
            middle_name=validated_data.get('middle_name', ''),
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            mob_number=validated_data['mob_number'],
            perm_add_village=validated_data['perm_add_village'],
            perm_add_gewog=validated_data['perm_add_gewog'],
            perm_add_dzongkhag=validated_data['perm_add_dzongkhag'],
            user_code=validated_data['user_code'],
            ps_add_village=validated_data['ps_add_village'],
            ps_add_gewog=validated_data['ps_add_gewog'],
            ps_add_dzongkhag=validated_data['ps_add_dzongkhag'],
            father_name=validated_data.get('father_name', ''),
            mother_name=validated_data.get('mother_name', ''),
            parent_occupation=validated_data.get('parent_occupation', ''),
            guardian_name=validated_data.get('guardian_name', ''),
            guardian_occupation=validated_data.get('guardian_occupation', ''),
            parent_status=validated_data.get('parent_status', ''),
            current_living_with=validated_data.get('current_living_with', ''),
            agency_code=validated_data['agency_code'],
            user_role_agency=validated_data['user_role_agency'],
            agency_name=validated_data['agency_name'],
            user_class=validated_data.get('user_class', ''),
            user_sub_class=validated_data.get('user_sub_class', ''),
            academy_code=validated_data.get('academy_code', ''),
            status=validated_data.get('status', True),
            # Hash the user's password
            password=make_password(validated_data['password']),
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        # Overriding the default update method to handle password hashing
        instance.password = make_password(validated_data.get('password', instance.password))
        # For all other fields, use the default handling (which calls setattr)
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
        agency = Agency.objects.create(**validated_data)
        return agency

    def update(self, instance, validated_data):
        # Update each field in the instance with validated data
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

