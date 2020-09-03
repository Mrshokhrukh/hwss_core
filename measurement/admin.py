from django.contrib import admin

from measurement.models import (
    ActiveUser,
    LifetimeUser,
    Measurement,
    MeasurementAssist,
    MeasurementSubstance,
    Submission,
    TestType,
    UserSubmission,
)


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ("question", "answer", "score", "diagnosis", "created_at")
    fields = ("question", "answer", "diagnosis", "score", "substance", "created_at")
    show_change_link = True


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "user_submission",
        "question_set",
        "question",
        "diagnosis",
        "substance",
        "score",
        "created_at",
    )
    list_filter = ("diagnosis", "score", "created_at", "substance")
    search_fields = (
        "user_submission__user__username",
        "question",
        "diagnosis",
        "substance",
    )
    readonly_fields = ("created_at",)
    actions = ["mark_as_high_risk"]

    def mark_as_high_risk(self, request, queryset):
        updated = queryset.update(diagnosis="High Risk")
        self.message_user(request, f"{updated} submissions were marked as 'High Risk'.")

    mark_as_high_risk.short_description = "Mark selected diagnosis as 'High Risk'"


class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test_type",
        "created_at",
        "rescreened",
        "mark_as_safe",
        "is_old_case",
        "get_diagnosis_summary",
    )
    list_filter = (
        "test_type",
        "created_at",
        "rescreened",
        "mark_as_safe",
        "is_old_case",
    )
    search_fields = ("user__username", "test_type__name")
    readonly_fields = ("created_at",)
    inlines = [SubmissionInline]

    def get_diagnosis_summary(self, obj):
        # Filter out empty diagnosis and remove duplicates
        diagnosis = obj.submission.values_list("diagnosis", flat=True)
        diagnosis = list(filter(None, diagnosis))  # Remove empty values
        return ", ".join(set(diagnosis)) if diagnosis else "No diagnosis"

    get_diagnosis_summary.short_description = "diagnosis Summary"


admin.site.register(TestType)
admin.site.register(UserSubmission, UserSubmissionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(MeasurementSubstance)
admin.site.register(MeasurementAssist)
admin.site.register(Measurement)
admin.site.register(LifetimeUser)
admin.site.register(ActiveUser)
