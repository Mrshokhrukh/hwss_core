from django.contrib import admin
from .models import (
    ActiveSubstanceUser, LifeTimeSubstanceUser, Notification, ServiceAndTreatment, 
    ServiceAndTreatmentHistory, Referral, Substance, Rescreening, 
    SubstanceRiskMeasurement, FinalUserSubmission
)

@admin.action(description="Duplicate selected records")
def duplicate_records(modeladmin, request, queryset):
    for obj in queryset:
        # Duplicate the record by copying all fields except `id` and `updated_at`
        obj.id = None  # Set id to None so it creates a new record
        obj.updated_at = None  # Reset updated_at if you want to
        obj.save()  # Save the new duplicated record

@admin.register(ServiceAndTreatment)
class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'updated_at', 'referred')
    list_filter = ('assessment_status', 'case_status', 'counseling', 'follow_up', 'referred','user__perm_add_dzongkhag', 'user__ps_add_dzongkhag')
    search_fields = ('user__username', 'updated_by__username', 'comments')
    date_hierarchy = 'date'
    readonly_fields = ('updated_at',)
    actions = [duplicate_records]  # Add the duplicate action here

@admin.register(ServiceAndTreatmentHistory)
class ServiceAndTreatmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('service_and_treatment', 'updated_by', 'updated_at')
    list_filter = ('updated_by',)
    search_fields = ('service_and_treatment__user__username', 'updated_by__username')
    readonly_fields = ('updated_at',)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by', 'referred_to_name', 'referral_status', 'date')
    list_filter = ('referral_status',)
    search_fields = ('user__username', 'referred_by__username', 'referred_to_name', 'referral_remarks')
    readonly_fields = ('date', 'referred_to_name')

@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Rescreening)
class RescreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'screened_by', 'rescreening_date', 'rescreening_count', 'rescreened')
    list_filter = ('rescreened', 'screened_by')
    search_fields = ('user__username', 'screened_by__username')
    date_hierarchy = 'rescreening_date'
    readonly_fields = ('rescreening_date',)

@admin.register(SubstanceRiskMeasurement)
class SubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'rescreening', 'measurement', 'risk_flag', 'total_score')
    list_filter = ('substance',)
    search_fields = ('substance__name', 'rescreening__user__username')
    
@admin.register(FinalUserSubmission)
class FinalUserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'initial_submission', 'phq_score', 'gad_score', 'ace_score', 'rescreened', 'submission_date')
    list_filter = ('rescreened',)
    search_fields = ('user__username', 'initial_submission__user__username')
    date_hierarchy = 'submission_date'
    readonly_fields = ('submission_date',)

@admin.register(LifeTimeSubstanceUser)
class LifeTimeSubstanceUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'screening_data', 'assessment', 'substances_display')
    search_fields = ('user__username',)
    list_filter = ('screening_data_type', 'assessment_type')
    
    def substances_display(self, obj):
        return ', '.join(obj.substances.keys()) if obj.substances else "No substances"
    substances_display.short_description = 'Substances Used'

@admin.register(ActiveSubstanceUser)
class ActiveSubstanceUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'screening_data', 'assessment', 'substances_display')
    search_fields = ('user__username',)
    list_filter = ('screening_data_type', 'assessment_type')
    
    def substances_display(self, obj):
        return ', '.join(obj.substances.keys()) if obj.substances else "No substances"
    substances_display.short_description = 'Substances Used'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_for', 'notification', 'notification_status', 'created_at', 'updated_at')
    list_filter = ('notification_status', 'created_at')
    search_fields = ('notification_for__email', 'notification', 'notification_for__first_name', 'notification_for__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('notification_for', 'notification', 'notification_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        # Customize queryset to include related user fields for efficient search
        return super().get_queryset(request).select_related('notification_for')