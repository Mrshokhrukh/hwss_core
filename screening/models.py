from django.db import models
from django.contrib.auth import get_user_model
from measurement.models import UserSubmission
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
    
    date = models.DateField()

    counselor = models.CharField(max_length=255)

    registration_lockout_end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Check if it's a new instance
            # Check if the user has reached the daily registration limit
            today = timezone.now().date()
            if self.user.case_screenings.filter(date=today).count() >= 10:
                self.user.is_locked = True
            else:
                # Increment the count of cases registered today
                self.user.cases_registered_today = self.user.case_screenings.filter(date=today).count() + 1

            # Calculate the end time of the registration lockout period
            self.registration_lockout_end_time = timezone.now() + timezone.timedelta(hours=24)  # Lockout for 24 hours
        
        super().save(*args, **kwargs)


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

    registration_lockout_end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id: 
            self.registration_lockout_end_time = timezone.now() + timezone.timedelta(days=self.duration)

        current_date = timezone.now().date()
        if current_date >= self.end_date or (self.registration_lockout_end_time and timezone.now() >= self.registration_lockout_end_time):
            self.approval_status = 'ended'

        super().save(*args, **kwargs)

class ScreenedUser(models.Model):
    event_screening = models.ForeignKey(EventScreening, on_delete=models.CASCADE, related_name='screened_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    screening_date = models.DateField(default=timezone.now)