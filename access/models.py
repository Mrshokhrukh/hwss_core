from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import random
import string
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, identity_number, first_name, last_name, date_of_birth, gender, mob_number, perm_add_village, perm_add_gewog, perm_add_dzongkhag, password=None, role=None, agency_data=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            identity_number=identity_number,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            mob_number=mob_number,
            perm_add_village=perm_add_village,
            perm_add_gewog=perm_add_gewog,
            perm_add_dzongkhag=perm_add_dzongkhag,
            role=role,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        # Create the associated agency user details
        if agency_data:
            agency = Agency.objects.create(**agency_data)
            UserAgency.objects.create(user=user, agency=agency)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password=password, **extra_fields)


class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    agency_code = models.CharField(max_length=100, unique=True)
    agency_name = models.CharField(max_length=100)
    agency_parent = models.CharField(max_length=100, null=True, blank=True)
    present_dzongkhag = models.CharField(max_length=100, null=True, blank=True)
    present_gewog = models.CharField(max_length=100, null=True, blank=True)
    present_village = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.agency_name


class UserAgency(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='agency_details')
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    user_code = models.CharField(max_length=100)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(
        max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(
        max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_stream = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.agency.agency_name}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    identity_number = models.CharField(max_length=50, unique=True)
    nationality = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True, null=True)
    mob_number = models.CharField(max_length=15, null=True, blank=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    active_agency = models.ForeignKey(
        'Agency', on_delete=models.SET_NULL, null=True, blank=True)
    ps_add_village = models.CharField(max_length=100, blank=True, null=True)
    ps_add_gewog = models.CharField(max_length=100, blank=True, null=True)
    ps_add_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    is_gyalsung = models.BooleanField(default=False)
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    ROLE_STUDENT = 'student'
    ROLE_CLINICAL_COUNSELOR = 'clinical_counselor'
    ROLE_SCHOOL_COUNSELOR = 'school_counselor'
    ROLE_ADMIN = 'admin'
    ROLE_RD_ADMIN = 'rd_admin'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_CLINICAL_COUNSELOR, 'Clinical Counselor'),
        (ROLE_SCHOOL_COUNSELOR, 'School Counselor'),
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_RD_ADMIN, 'R&D Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)
    access_level = models.IntegerField(default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['identity_number', 'email', 'first_name', 'last_name', 'date_of_birth',
                       'gender', 'mob_number', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag']

    objects = CustomUserManager()

    def __str__(self):
        return self.username or f"CustomUser #{self.pk}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class PreRecordedUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    identity_number = models.CharField(max_length=50, unique=True)
    nationality = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    mob_number = models.CharField(max_length=15)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    is_gyalsung = models.BooleanField(default=False)
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100, blank=True, null=True)
    access_level = models.CharField(max_length=100, blank=True, null=True)
    # New field to indicate registration status
    is_registered = models.BooleanField(default=False)

    # New fields to match user_data and agency_data
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    agency_code = models.CharField(max_length=100, blank=True, null=True)

    # User agency data
    user_code = models.CharField(max_length=100, blank=True, null=True)
    ps_add_village = models.CharField(max_length=100, blank=True, null=True)
    ps_add_gewog = models.CharField(max_length=100, blank=True, null=True)
    ps_add_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(
        max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(
        max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100, blank=True, null=True)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Pre-recorded user'
        verbose_name_plural = 'Pre-recorded users'
