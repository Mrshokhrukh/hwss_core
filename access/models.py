from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import random
import string
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, identity_number, first_name, last_name, date_of_birth, gender, mob_number, perm_add_village, perm_add_gewog, perm_add_dzongkhag, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        # Generate a temporary unique username
        temporary_username = str(uuid.uuid4())

        email = self.normalize_email(email)
        user = self.model(
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
            **extra_fields,
        )
        user.username = temporary_username  # Set the username separately
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_gyalsung = models.BooleanField(default=False)
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
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['identity_number', 'first_name', 'last_name', 'date_of_birth', 'gender', 'mob_number', 'email', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Agency(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agency')
    user_code = models.CharField(max_length=100)
    ps_add_village = models.CharField(max_length=100)
    ps_add_gewog = models.CharField(max_length=100)
    ps_add_dzongkhag = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    agency_code = models.CharField(max_length=100)
    user_role_agency = models.CharField(max_length=100)
    agency_name = models.CharField(max_length=100)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.agency_name}"


class PreRecordedUser(models.Model):
    identity_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    mob_number = models.CharField(max_length=15)
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Pre-recorded user'
        verbose_name_plural = 'Pre-recorded users'

class PreRecordedAgency(models.Model):
    prerecorded_user = models.ForeignKey(PreRecordedUser, on_delete=models.CASCADE, related_name='prerecorded_agency')
    user_code = models.CharField(max_length=100)
    ps_add_village = models.CharField(max_length=100)
    ps_add_gewog = models.CharField(max_length=100)
    ps_add_dzongkhag = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    agency_code = models.CharField(max_length=100)
    user_role_agency = models.CharField(max_length=100)
    agency_name = models.CharField(max_length=100)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pre-recorded agency'
        verbose_name_plural = 'Pre-recorded agencies'