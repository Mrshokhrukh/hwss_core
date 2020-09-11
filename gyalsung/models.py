from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

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

    # Use CharField for CID/identity number instead of ForeignKey
    identity_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="CID/Identity number of the user",
    )

    # Keep the user field for backward compatibility but make it optional
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gyalsung_assessments",
        null=True,
        blank=True,
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
        max_length=10, choices=SCREENING_STATUS_CHOICES, default="", blank=True
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

    def clean(self):
        """Validate that either user or identity_number is provided."""
        if not self.user and not self.identity_number:
            raise ValidationError("Either user or identity_number must be provided.")
        if self.user and self.identity_number:
            # Ensure consistency
            if self.user.identity_number != self.identity_number:
                raise ValidationError(
                    "User's identity number doesn't match the provided identity_number."
                )

    def save(self, *args, **kwargs):
        """Auto-populate user field if identity_number is provided."""
        if self.identity_number and not self.user:
            try:
                self.user = User.objects.get(identity_number=self.identity_number)
            except User.DoesNotExist:
                # You might want to handle this case differently
                # For now, we'll just save without the user
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        user_identifier = self.user.username if self.user else self.identity_number
        return f"Gyalsung Assessment for {user_identifier} (Status: {self.final_screening_status})"

    @property
    def username(self):
        """Return username if user exists, otherwise return identity number."""
        return self.user.username if self.user else self.identity_number

    @property
    def user_details(self):
        """Return user details if available."""
        if self.user:
            return {
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            }
        return {
            "username": self.identity_number,
            "first_name": "Unknown",
            "last_name": "User",
            "email": "",
        }


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
