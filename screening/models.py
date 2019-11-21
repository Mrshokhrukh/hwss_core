from django.db import models
from django.contrib.auth import get_user_model
from access.models import CustomUser
from measurement.models import UserSubmission
from monitoring.models import Referral, ServiceAndTreatment
from django.utils import timezone

User = get_user_model()

class CaseScreening(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_screenings')
    case_name = models.CharField(max_length=255)
    PURPOSE_CHOICES = [
        ('assessment', 'Assessment'),
        ('intervention', 'Intervention'),
        ('follow_up', 'Follow Up'),
        ('termination', 'Termination'),
    ]
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    submission = models.ForeignKey(UserSubmission, on_delete=models.SET_NULL, null=True, blank=True)
    DZONGKHAG_CHOICES = [
        ('Bumthang', 'Bumthang'),
        ('Chukha', 'Chukha'),
        ('Dagana', 'Dagana'),
        ('Gasa', 'Gasa'),
        ('Haa', 'Haa'),
        ('Lhuentse', 'Lhuentse'),
        ('Mongar', 'Mongar'),
        ('Paro', 'Paro'),
        ('Pemagatshel', 'Pemagatshel'),
        ('Punakha', 'Punakha'),
        ('Samdrup Jongkhar', 'Samdrup Jongkhar'),
        ('Samtse', 'Samtse'),
        ('Sarpang', 'Sarpang'),
        ('Thimphu', 'Thimphu'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Trongsa', 'Trongsa'),
        ('Tsirang', 'Tsirang'),
        ('Wangdue Phodrang', 'Wangdue Phodrang'),
        ('Zhemgang', 'Zhemgang'),
    ]
    dzongkhag = models.CharField(max_length=50, choices=DZONGKHAG_CHOICES)
    date = models.DateField(null=True, blank=True)
    counselor = models.CharField(max_length=255)
    registration_lockout_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Case Screening: {self.case_name}"

    
    def save(self, *args, **kwargs):
        if not self.id: 
            today = timezone.now().date()
            if self.user.case_screenings.filter(date=today).count() >= 10:
                self.user.is_locked = True
            else:
                self.user.cases_registered_today = self.user.case_screenings.filter(date=today).count() + 1
            self.registration_lockout_end_time = timezone.now() + timezone.timedelta(hours=24) 
        super().save(*args, **kwargs)

class ScreenedUser(models.Model):
    event_screening = models.ForeignKey('EventScreening', on_delete=models.CASCADE, related_name='screened_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    screening_date = models.DateField(default=timezone.now)



class CaseBasedSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Add a ForeignKey field to the User model
    case = models.ForeignKey(
        CaseScreening, on_delete=models.CASCADE, related_name='case_based_submissions')
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
    submission_date = models.DateTimeField(auto_now_add=True)
    service_and_treatment = models.ForeignKey(
        'monitoring.ServiceAndTreatment', on_delete=models.SET_NULL, related_name='case_based_submissions', null=True, blank=True)
    referral = models.ForeignKey(
        'monitoring.Referral', on_delete=models.SET_NULL, related_name='case_based_submissions', null=True, blank=True)

    def __str__(self):
        return f"Case Based Submission for {self.case}"


class CaseSubstance(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class CaseSubstanceRiskMeasurement(models.Model):
    substance = models.ForeignKey(
        CaseSubstance, on_delete=models.CASCADE, related_name='case_risk_measurements')
    case_submission = models.ForeignKey(
        CaseBasedSubmission, on_delete=models.CASCADE, related_name='case_substance_risk_measurements')
    measurement = models.FloatField(help_text="Measurement value for the substance")
    risk_flag = models.CharField(max_length=250, help_text="Risk flag based on measurement")
    total_score = models.FloatField(help_text="Total score for the substance", null=True, blank=True)  

    def __str__(self):
        return f"Risk Measurement for {self.substance} in Case Based Submission for {self.case_submission.case.case_name}"
    

class EventScreening(models.Model):
    event_name = models.CharField(max_length=255)
    event_purpose = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in hours")
    counselor = models.CharField(max_length=255)
    approval_status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('ended', 'Ended'),
    ]
    approval_status = models.CharField(max_length=20, choices=approval_status_choices, default='pending')
    remarks = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    registration_lockout_end_time = models.DateTimeField(null=True, blank=True)
    selected_tool = models.CharField(max_length=100, null=True, blank=True)
    users = models.ManyToManyField(CustomUser, related_name='events', blank=True)

    # Add the created_by field
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='event_screenings',
        null=True,  # Set to True if you have existing data
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.registration_lockout_end_time = timezone.now() + timezone.timedelta(days=self.duration)

        current_date = timezone.now().date()
        if current_date >= self.end_date or (self.registration_lockout_end_time and timezone.now() >= self.registration_lockout_end_time):
            self.approval_status = 'ended'

        super().save(*args, **kwargs)


class EventBasedSubmission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='event_based_submissions')
    event = models.ForeignKey(
        EventScreening, on_delete=models.CASCADE, related_name='event_based_submissions')
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
    submission_date = models.DateTimeField(auto_now_add=True)
    service_and_treatment = models.ForeignKey(
        'monitoring.ServiceAndTreatment', on_delete=models.SET_NULL, related_name='event_based_submissions', null=True, blank=True)
    referral = models.ForeignKey(
        'monitoring.Referral', on_delete=models.SET_NULL, related_name='event_based_submissions', null=True, blank=True)

    def __str__(self):
        return f"Event Based Submission for {self.event.event_name}"

class EventSubstance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EventSubstanceRiskMeasurement(models.Model):
    substance = models.ForeignKey(
        EventSubstance, on_delete=models.CASCADE, related_name='event_risk_measurements')
    event_submission = models.ForeignKey(
        EventBasedSubmission, on_delete=models.CASCADE, related_name='event_substance_risk_measurements')
    measurement = models.FloatField(help_text="Measurement value for the substance")
    risk_flag = models.CharField(max_length=250, help_text="Risk flag based on measurement")
    total_score = models.FloatField(help_text="Total score for the substance", null=True, blank=True)  

    def __str__(self):
        return f"Risk Measurement for {self.substance} in Event Based Submission for {self.event_submission.event.event_name}"


