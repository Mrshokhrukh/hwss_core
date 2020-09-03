from django.contrib import admin

from gyalsung.models import (
    GyalsungAssessment,
    GyalsungEventSubstanceRiskMeasurement,
    GyalsungUserScreeningHistory,
)


@admin.register(GyalsungUserScreeningHistory)
class GyalsungUserScreeningHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
        "latest_assessment_display",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("event_submission", "case_submission", "gyalsung_assessments")

    def latest_assessment_display(self, obj):
        latest = obj.latest_gyalsung_assessment()
        return latest.submission_date if latest else "—"

    latest_assessment_display.short_description = "Latest Assessment"


@admin.register(GyalsungAssessment)
class GyalsungAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "gad_score",
        "phq_score",
        "ace_score",
        "psy_score",
        "final_screening_status",
        "is_reassessment_screening",
        "submission_date",
        "created_at",
    )
    list_filter = (
        "final_screening_status",
        "is_reassessment_screening",
        "submission_date",
    )
    search_fields = ("user__username", "user__email")
    autocomplete_fields = ("user", "counselor_user", "reassessment_user")


@admin.register(GyalsungEventSubstanceRiskMeasurement)
class GyalsungEventSubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "substance",
        "assessment_submission",
        "measurement",
        "risk_flag",
        "total_score",
    )
    list_filter = ("risk_flag",)
    search_fields = ("substance__name", "assessment_submission__user__username")
    autocomplete_fields = ("substance", "assessment_submission")
