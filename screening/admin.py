from django.contrib import admin
from .models import CaseScreening, EventScreening, ScreenedUser, EventBasedSubmission, CaseBasedSubmission, EventSubstance, EventSubstanceRiskMeasurement, CaseSubstance, CaseSubstanceRiskMeasurement

class CaseScreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'case_name', 'purpose', 'dzongkhag', 'date', 'counselor')
    list_filter = ('purpose', 'dzongkhag', 'date')
    search_fields = ('user__username', 'case_name', 'counselor')
    date_hierarchy = 'date'

admin.site.register(CaseScreening, CaseScreeningAdmin)

class EventScreeningAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_purpose', 'location', 'start_date', 'end_date', 'counselor', 'approval_status')
    list_filter = ('start_date', 'end_date', 'approval_status')
    search_fields = ('event_name', 'location', 'counselor')
    date_hierarchy = 'start_date'

admin.site.register(EventScreening, EventScreeningAdmin)

class ScreenedUserAdmin(admin.ModelAdmin):
    list_display = ('event_screening', 'user', 'screening_date')
    list_filter = ('screening_date',)
    search_fields = ('event_screening__event_name', 'user__username')
    date_hierarchy = 'screening_date'

admin.site.register(ScreenedUser, ScreenedUserAdmin)

class EventBasedSubmissionAdmin(admin.ModelAdmin):
    list_display = ('event', 'submission_date')
    list_filter = ('submission_date',)
    search_fields = ('event__name',)
    date_hierarchy = 'submission_date'

admin.site.register(EventBasedSubmission, EventBasedSubmissionAdmin)


class CaseBasedSubmissionAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'case', 'submission_date')  # Replace 'user' with a callable method
    list_filter = ('submission_date',)
    search_fields = ('case__name',)
    date_hierarchy = 'submission_date'

    def get_user_name(self, obj):
        return obj.user.username  # Assuming 'user' is a ForeignKey to a User model

    get_user_name.short_description = 'User'  # Set a user-friendly name for the column

admin.site.register(CaseBasedSubmission, CaseBasedSubmissionAdmin)

class EventSubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(EventSubstance, EventSubstanceAdmin)

class EventSubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'event_submission', 'measurement', 'risk_flag', 'total_score')
    list_filter = ('measurement', 'risk_flag', 'total_score')
    search_fields = ('substance__name', 'event_submission__event__name')
    date_hierarchy = 'event_submission__submission_date'

admin.site.register(EventSubstanceRiskMeasurement, EventSubstanceRiskMeasurementAdmin)

class CaseSubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(CaseSubstance, CaseSubstanceAdmin)

class CaseSubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'case_submission', 'measurement', 'risk_flag', 'total_score')
    list_filter = ('measurement', 'risk_flag', 'total_score')
    search_fields = ('substance__name', 'case_submission__case__name')
    date_hierarchy = 'case_submission__submission_date'

admin.site.register(CaseSubstanceRiskMeasurement, CaseSubstanceRiskMeasurementAdmin)
