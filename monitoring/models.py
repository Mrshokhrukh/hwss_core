from django.db import models
from django.utils import timezone
from access.models import CustomUser
from multiselectfield import MultiSelectField
from measurement.models import Submission, Measurement, MeasurementAssist


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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # You might want to adjust this field accordingly
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
    service_and_treatment = models.ForeignKey(ServiceAndTreatment, on_delete=models.CASCADE, related_name='referrals', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.referred_to:
            self.referred_to_name = f"{self.referred_to.first_name} {self.referred_to.middle_name} {self.referred_to.last_name}"
        super().save(*args, **kwargs)


class Rescreening(models.Model):
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    submission_diagnosis = models.CharField(max_length=255)
    measurement = models.JSONField()  
    measurement_assist = models.JSONField()
    service_and_treatment = models.ForeignKey(ServiceAndTreatment, on_delete=models.CASCADE, related_name='rescreenings', null=True, blank=True)
    
    # New field to track rescreening count
    rescreening_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Rescreening for {self.user.username}"