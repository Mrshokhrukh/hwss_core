from django.db import models
from django.utils import timezone
from access.models import CustomUser
from multiselectfield import MultiSelectField
from measurement.models import Submission, Measurement, MeasurementAssist
from django.contrib.auth import get_user_model

User = CustomUser

class ServiceAndTreatment(models.Model):
    DATE_CHOICES = (
        ('Not Conducted', 'Not Conducted'),
        ('Conducted', 'Conducted'),
    )
    ASSESSMENT_STATUS_CHOICES = (
        ('Not Conducted', 'Not Conducted'),
        ('Conducted', 'Conducted'),
    )
    CASE_STATUS_CHOICES = (
        ('On Going', 'On Going'),
        ('Case Closed', 'Case Closed'),
        ('Case Discontinued', 'Case Discontinued'),
    )
    COUNSELLING_CHOICES = (
        ('Availed', 'Availed'),
        ('Not Required', 'Not Required'),
        ('Waiting List', 'Waiting List'),
    )
    FOLLOW_UP_CHOICES = (
        ('Treatment Completed', 'Treatment Completed'),
        ('Undergoing Treatment', 'Undergoing Treatment'),
        ('Completed Counselling Sessions', 'Completed Counselling Sessions'),
        ('Unwilling to Undergo Treatment', 'Unwilling to Undergo Treatment'),
        ('Undergone Rehabilitation', 'Undergone Rehabilitation'),
        ('Undergoing Rehabilitation', 'Undergoing Rehabilitation'),
        ('Hospital-based Outpatient SUD Treatment and Care (Primary Phase)',
         'Hospital-based Outpatient SUD Treatment and Care (Primary Phase)'),
        ('Hospital-based Outpatient SUD Treatment and Care (Continuing Care)',
         'Hospital-based Outpatient SUD Treatment and Care (Continuing Care)'),
        ('School-based SUD Treatment and Care',
         'School-based SUD Treatment and Care'),
        ('Institution-based SUD Treatment and Care',
         'Institution-based SUD Treatment and Care'),
        ('Follow-up Drug Test Conducted', 'Follow-up Drug Test Conducted'),
        ('Detention-based SUD Treatment and Care',
         'Detention-based SUD Treatment and Care'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(default=None)
    assessment_status = models.CharField(
        max_length=20, choices=ASSESSMENT_STATUS_CHOICES, default='Not Conducted')
    case_status = models.CharField(
        max_length=20, choices=CASE_STATUS_CHOICES, default='On Going')
    counseling = models.CharField(
        max_length=20, choices=COUNSELLING_CHOICES, default='Waiting List')
    follow_up = models.CharField(
        max_length=255, choices=FOLLOW_UP_CHOICES, blank=True)
    comments = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='updated_by')
    updated_at = models.DateTimeField(default=timezone.now)

class ServiceAndTreatmentHistory(models.Model):
    service_and_treatment = models.ForeignKey(ServiceAndTreatment, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='service_and_treatment_histories')
    updated_at = models.DateTimeField(default=timezone.now)
    changes = models.TextField()


class Referral(models.Model):
    REFERRAL_STATUS_CHOICES = (
        ('Awaiting', 'Awaiting'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    referred_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='referrals_received', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    referred_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='referrals_made', null=True, blank=True)
    referred_to_name = models.CharField(max_length=100, null=True, blank=True)
    referral_status = models.CharField(
        max_length=20, choices=REFERRAL_STATUS_CHOICES, default='Awaiting')
    referral_remarks = models.TextField(null=True, blank=True)
    service_and_treatment = models.ForeignKey(
        ServiceAndTreatment, on_delete=models.CASCADE, related_name='referrals', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.referred_to:
            self.referred_to_name = f"{self.referred_to.first_name} {self.referred_to.middle_name} {self.referred_to.last_name}"
        super().save(*args, **kwargs)


class Substance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Rescreening(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='rescreenings')
    gad_data = models.JSONField(null=True, blank=True)
    gad_score = models.IntegerField(null=True, blank=True)
    gad_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of GAD score")
    phq_data = models.JSONField(null=True, blank=True)
    phq_score = models.IntegerField(null=True, blank=True)
    phq_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of PHQ score")
    ace_data = models.JSONField(null=True, blank=True)
    ace_score = models.IntegerField(null=True, blank=True)
    ace_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of ACE score")
    school_env_data = models.JSONField(null=True, blank=True)
    rescreened = models.BooleanField(default=False)
    rescreening_count = models.IntegerField(default=0, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    service_and_treatment = models.ForeignKey(
        'ServiceAndTreatment', on_delete=models.SET_NULL, related_name='rescreenings', null=True, blank=True)
    referral = models.ForeignKey(
        'Referral', on_delete=models.SET_NULL, related_name='rescreenings', null=True, blank=True)

    def __str__(self):
        return f"Rescreening for {self.user.username}"


class SubstanceRiskMeasurement(models.Model):
    substance = models.ForeignKey(
        Substance, on_delete=models.CASCADE, related_name='risk_measurements')
    rescreening = models.ForeignKey(
        Rescreening, on_delete=models.CASCADE, related_name='substance_risk_measurements')
    measurement = models.FloatField(help_text="Measurement value for the substance")
    risk_flag = models.CharField(max_length=250, help_text="Risk flag based on measurement")
    total_score = models.FloatField(help_text="Total score for the substance", null=True, blank=True)  # Add a new field for total score

    def __str__(self):
        return f"Risk Measurement for {self.substance} in Rescreening for {self.rescreening.user.username}"
