from django.contrib import admin

from reporting.models import Reporting, ReportingModel


class ReportingAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "agency_code",
        "agency_name",
        "present_dzongkhag",
        "present_gewog",
        "present_village",
        "user_code",
        "assessment_status",
        "case_status",
        "counseling",
        "follow_up",
        "referral_status",
        "referral_remarks",
    ]
    search_fields = [
        "user__username",
        "agency_code",
        "agency_name",
        "present_dzongkhag",
        "present_gewog",
        "present_village",
        "user_code",
        "assessment_status",
        "case_status",
        "counseling",
        "follow_up",
        "referral_status",
        "referral_remarks",
    ]
    list_filter = ["assessment_status", "case_status", "counseling", "referral_status"]
    list_per_page = 20


class ReportingModelAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "user_agency",
        "agency",
        "agency_name",
        "service_and_treatment",
        "referral",
        "measurement",
        "measurement_assist",
        "rescreened",
        "rescreened_by",
        "original_submission_date",
        "rescreened_date",
    ]
    search_fields = [
        "user__username",
        "user_agency__user__email",
        "agency__agency_name",
        "agency_name",
        "service_and_treatment__date",
        "referral__date",
        "rescreened_by__username",
        "original_submission_date",
        "rescreened_date",
    ]
    list_filter = ["agency"]
    list_per_page = 20


admin.site.register(ReportingModel, ReportingModelAdmin)
admin.site.register(Reporting, ReportingAdmin)
