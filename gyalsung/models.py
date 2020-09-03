from django.contrib.auth import get_user_model
from django.db import models

from gyalsung.constants import SCREENING_STATUS_CHOICES
from screening.models import CaseBasedSubmission, EventBasedSubmission, EventSubstance

User = get_user_model()


class GyalsungUserScreeningHistory(models.Model):
    """Stores all screenings (event, case, gyalsung) a user has participated in."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="screening_history"
    )
    event_submission = models.ManyToManyField(EventBasedSubmission, blank=True)
    case_submission = models.ManyToManyField(CaseBasedSubmission, blank=True)
    gyalsung_assessments = models.ManyToManyField(
        "GyalsungAssessment", blank=True, related_name="users"
    )

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gyalsung User Screening History"
        verbose_name_plural = "Gyalsung User Screening Histories"

    def __str__(self):
        return f"Screening history for {self.user}"

    def latest_gyalsung_assessment(self):
        """Get the latest GyalsungAssessment for this user."""
        return self.gyalsung_assessments.order_by("-created_at").first()


class GyalsungAssessment(models.Model):
    """Represents a Gyalsung-specific assessment (questions + score)."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gyalsung_assessments"
    )

    gad_data = models.JSONField(null=True, blank=True)
    gad_score = models.IntegerField(null=True, blank=True)
    gad_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of GAD score"
    )
    phq_data = models.JSONField(null=True, blank=True)
    phq_score = models.IntegerField(null=True, blank=True)
    phq_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of PHQ score"
    )
    ace_data = models.JSONField(null=True, blank=True)
    ace_score = models.IntegerField(null=True, blank=True)
    ace_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of ACE score"
    )
    psy_data = models.JSONField(null=True, blank=True)
    psy_score = models.IntegerField(null=True, blank=True)
    psy_interpretation = models.CharField(
        max_length=255, null=True, blank=True, help_text="Interpretation of PSY score"
    )
    submission_date = models.DateTimeField(auto_now_add=True)

    final_screening_status = models.CharField(
        max_length=10, choices=SCREENING_STATUS_CHOICES, default=""
    )
    is_reassessment_screening = models.BooleanField(default=False)
    # Counselor + Reassessment
    counselor_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="counseled_assessments",
    )
    reassessment_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reassessed_assessments",
    )
    counselor_remarks = models.TextField(blank=True, null=True)
    reassessment_remarks = models.TextField(blank=True, null=True)

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gyalsung Assessment for {self.user.username} (Score: {self.score}, Status: {self.status})"


class GyalsungEventSubstanceRiskMeasurement(models.Model):
    substance = models.ForeignKey(
        EventSubstance,
        on_delete=models.CASCADE,
        related_name="gyalsung_risk_measurements",
    )
    assessment_submission = models.ForeignKey(
        GyalsungAssessment,
        on_delete=models.CASCADE,
        related_name="gyalsung_assessment_risk_measurements",
    )
    measurement = models.FloatField(help_text="Measurement value for the substance")
    risk_flag = models.CharField(
        max_length=250, help_text="Risk flag based on measurement"
    )
    total_score = models.FloatField(
        help_text="Total score for the substance", null=True, blank=True
    )

    def __str__(self):
        return f"Risk Measurement for {self.substance} in the Gyalsung Assessment. "
