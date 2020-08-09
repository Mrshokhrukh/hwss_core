from django.db import models
from django.utils import timezone

from access.models import CustomUser
from measurement.constants import (
    ACE_CHOICES,
    FLAG_CHOICES,
    GAD_FLAG_CHOICES,
    GAD_MEASUREMENT_CHOICES,
    INJECTION_FLAG_CHOICES,
    INJECTION_RISK_CHOICES,
    PHQ_FLAG_CHOICES,
    PHQ_MEASUREMENT_CHOICES,
    RISK_CHOICES,
    SUICIDAL_CHOICES,
    SUICIDAL_FLAG_CHOICES,
)

OVERALL_FLAG_CHOICES = FLAG_CHOICES


class TestType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_type = models.ForeignKey(
        TestType, on_delete=models.CASCADE, related_name="usersubmission"
    )
    created_at = models.DateTimeField(default=timezone.now)
    rescreened = models.BooleanField(default=False)
    mark_as_safe = models.BooleanField(default=False)
    is_old_case = models.BooleanField(default=False)

    def __str__(self):
        unique_string = f'{self.user.username}_{self.test_type.name}_{self.created_at.strftime("%Y-%m-%d_%H")}'
        return unique_string


class QuestionSet(models.Model):
    name = models.CharField(max_length=100)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="questionset"
    )

    def __str__(self):
        return self.name


class Submission(models.Model):
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="submission"
    )
    question_set = models.ForeignKey(
        QuestionSet, on_delete=models.CASCADE, related_name="submission"
    )
    question = models.TextField()
    answer = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    substance = models.CharField(max_length=100)
    specify = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Submission for {self.user_submission.user.username}"


class MeasurementSubstance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MeasurementAssist(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="measurementassist"
    )
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="measurementassist"
    )

    # Alcoholic
    alcoholic_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    alcoholic_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    alcoholic_score = models.FloatField(null=True, blank=True)

    # Tobacco
    tobacco_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    tobacco_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    tobacco_score = models.FloatField(null=True, blank=True)

    # Cannabis
    cannabis_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    cannabis_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    cannabis_score = models.FloatField(null=True, blank=True)

    # Cocaine
    cocaine_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    cocaine_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    cocaine_score = models.FloatField(null=True, blank=True)

    # Amphetamine
    amphetamine_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    amphetamine_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    amphetamine_score = models.FloatField(null=True, blank=True)

    # Inhalants
    inhalants_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    inhalants_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    inhalants_score = models.FloatField(null=True, blank=True)

    # Sedatives
    sedatives_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    sedatives_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    sedatives_score = models.FloatField(null=True, blank=True)

    # Hallucinogens
    hallucinogens_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    hallucinogens_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    hallucinogens_score = models.FloatField(null=True, blank=True)

    # Opioids
    opioids_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    opioids_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    opioids_score = models.FloatField(null=True, blank=True)

    # Injection
    injection_measurement = models.CharField(
        max_length=50, choices=INJECTION_RISK_CHOICES, null=True, blank=True
    )
    injection_flag = models.CharField(
        max_length=50, choices=INJECTION_FLAG_CHOICES, null=True, blank=True
    )
    injection_score = models.FloatField(null=True, blank=True)

    # Other substances
    other_measurement = models.CharField(
        max_length=50, choices=RISK_CHOICES, null=True, blank=True
    )
    other_flag = models.CharField(
        max_length=50, choices=FLAG_CHOICES, null=True, blank=True
    )
    other_score = models.FloatField(null=True, blank=True)
    other_name = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"MeasurementAssist data for {self.user.username}"


class Measurement(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="measurement"
    )
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="measurement"
    )

    # GAD
    gad_measurement = models.CharField(
        max_length=50, choices=GAD_MEASUREMENT_CHOICES, null=True, blank=True
    )
    gad_flag = models.CharField(
        max_length=10, choices=GAD_FLAG_CHOICES, null=True, blank=True
    )
    gad_score = models.FloatField(null=True, blank=True)

    # PHQ
    phq_measurement = models.CharField(
        max_length=50, choices=PHQ_MEASUREMENT_CHOICES, null=True, blank=True
    )
    phq_flag = models.CharField(
        max_length=10, choices=PHQ_FLAG_CHOICES, null=True, blank=True
    )
    phq_score = models.FloatField(null=True, blank=True)

    # Suicidal
    suicidal_measurement = models.CharField(
        max_length=50, choices=SUICIDAL_CHOICES, null=True, blank=True
    )
    suicidal_flag = models.CharField(
        max_length=10, choices=SUICIDAL_FLAG_CHOICES, null=True, blank=True
    )
    suicidal_score = models.FloatField(null=True, blank=True)

    # ACE
    ace_measurement = models.CharField(
        max_length=50, choices=ACE_CHOICES, null=True, blank=True
    )
    ace_flag = models.CharField(
        max_length=10, choices=FLAG_CHOICES, null=True, blank=True
    )
    ace_score = models.FloatField(null=True, blank=True)

    # Overall
    overall_flag = models.CharField(
        max_length=10, choices=OVERALL_FLAG_CHOICES, null=True, blank=True
    )

    # ASSIST (ForeignKey to MeasurementAssist)
    assist = models.OneToOneField(
        MeasurementAssist, on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Measurement data for {self.user.username}"


class LifetimeUser(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="lifetime_user"
    )
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="lifetime_users"
    )
    substances_used = models.ManyToManyField(MeasurementSubstance, blank=True)

    def __str__(self):
        return f"Lifetime User: {self.user.username}"


class ActiveUser(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="active_user"
    )
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="active_users"
    )
    substances_used = models.ManyToManyField(MeasurementSubstance, blank=True)

    def __str__(self):
        return f"Active User: {self.user.username}"
