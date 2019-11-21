from django.db import models
from django.utils import timezone
from access.models import CustomUser
from multiselectfield import MultiSelectField
from measurement.models import Submission, Measurement, MeasurementAssist, UserSubmission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import JSONField
from django.utils.timezone import now

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
    REFERRED_CHOICES = (
        ('Awaiting', 'Awaiting'),
        ('Rejected', 'Rejected'),
        ('Referred', 'Referred'),
        ('Referred Back', 'Referred Back'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    assessment = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    assessment_status = models.CharField(
        max_length=20, choices=ASSESSMENT_STATUS_CHOICES, default='Not Conducted', null=True, blank=True)
    case_status = models.CharField(
        max_length=20, choices=CASE_STATUS_CHOICES, default='On Going', null=True, blank=True)
    counseling = models.CharField(
        max_length=20, choices=COUNSELLING_CHOICES, default='Waiting List', null=True, blank=True)
    follow_up = models.CharField(
        max_length=255, choices=FOLLOW_UP_CHOICES, blank=True, null=True)
    comments = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='updated_by')
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    referred = models.CharField(
        max_length=20, choices=REFERRED_CHOICES, default='Awaiting', null=True, blank=True)
    referral_instance = models.ForeignKey(
        'Referral', on_delete=models.CASCADE, related_name='service_and_treatments', null=True, blank=True)



class ServiceAndTreatmentHistory(models.Model):
    service_and_treatment = models.ForeignKey(
        ServiceAndTreatment, on_delete=models.CASCADE)
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

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    assessment = GenericForeignKey('content_type', 'object_id')

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
    service_and_treatment = models.OneToOneField(
        ServiceAndTreatment, on_delete=models.CASCADE, related_name='referral', null=True, blank=True
    )

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
    screened_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='screened_rescreenings', null=True, blank=True)
    rescreening_date = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        return f"Rescreening for {self.user.username}"


class SubstanceRiskMeasurement(models.Model):
    substance = models.ForeignKey(
        Substance, on_delete=models.CASCADE, related_name='risk_measurements')
    rescreening = models.ForeignKey(
        Rescreening, on_delete=models.CASCADE, related_name='substance_risk_measurements')
    measurement = models.FloatField(
        help_text="Measurement value for the substance")
    risk_flag = models.CharField(
        max_length=250, help_text="Risk flag based on measurement")
    total_score = models.FloatField(
        help_text="Total score for the substance", null=True, blank=True)

    def __str__(self):
        return f"Risk Measurement for {self.substance} in Rescreening for {self.rescreening.user.username}"


class FinalUserSubmission(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='final_submissions')
    initial_submission = models.ForeignKey(
        'measurement.UserSubmission', on_delete=models.SET_NULL, null=True, blank=True, related_name='final_submissions')

    phq_data = models.JSONField(null=True, blank=True)
    phq_score = models.IntegerField(null=True, blank=True)
    phq_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of PHQ score")

    gad_data = models.JSONField(null=True, blank=True)
    gad_score = models.IntegerField(null=True, blank=True)
    gad_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of GAD score")

    ace_data = models.JSONField(null=True, blank=True)
    ace_score = models.IntegerField(null=True, blank=True)
    ace_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of ACE score")

    assist_data = models.JSONField(null=True, blank=True)

    rescreened = models.BooleanField(default=True)
    rescreening_count = models.IntegerField(default=0, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    rescreened_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='final_rescreened_by'
    )

    # Relations to capture treatment history or services provided
    service_and_treatment = models.ForeignKey(
        'ServiceAndTreatment', on_delete=models.SET_NULL, related_name='final_submissions', null=True, blank=True
    )

    referral = models.ForeignKey(
        'Referral', on_delete=models.SET_NULL, null=True, blank=True, related_name='final_submissions'
    )

    def __str__(self):
        return f"Final submission for {self.user.username} on {self.submission_date.strftime('%Y-%m-%d')}"


class LifeTimeSubstanceUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    screening_data_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="lifetime_screening_data_type")
    object_id = models.PositiveIntegerField()
    screening_data = GenericForeignKey('screening_data_type', 'object_id')
    assessment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="lifetime_assessment_type")
    assessment_id = models.PositiveIntegerField()
    assessment = GenericForeignKey('assessment_type', 'assessment_id')
    substances = JSONField()

    def __str__(self):
        return f"Lifetime Substance Use for {self.user}"


class ActiveSubstanceUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    screening_data_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="active_screening_data_type")
    object_id = models.PositiveIntegerField()
    screening_data = GenericForeignKey('screening_data_type', 'object_id')
    assessment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="active_assessment_type")
    assessment_id = models.PositiveIntegerField()
    assessment = GenericForeignKey('assessment_type', 'assessment_id')
    substances = JSONField()

    def __str__(self):
        return f"Active Substance Use for {self.user}"
    

class Notification(models.Model):
    NOTIFICATION_STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    id = models.AutoField(primary_key=True)
    notification_for = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="The user for whom this notification is intended."
    )
    notification = models.TextField(help_text="The notification message.")
    notification_status = models.CharField(
        max_length=10,
        choices=NOTIFICATION_STATUS_CHOICES,
        default='unread',
        help_text="The status of the notification (unread/read)."
    )
    created_at = models.DateTimeField(default=now, help_text="The time when the notification was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The last time the notification was updated.")

    def mark_as_read(self):
        self.notification_status = 'read'
        self.save()

    def __str__(self):
        return f"Notification for {self.notification_for.email}: {self.notification[:50]}"

    class Meta:
        ordering = ['-created_at']