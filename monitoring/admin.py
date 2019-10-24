from django.contrib import admin
from .models import ServiceAndTreatment, ServiceAndTreatmentHistory, Referral, Substance, Rescreening, SubstanceRiskMeasurement, FinalUserSubmission

@admin.register(ServiceAndTreatment)
class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'updated_at', 'referred')
    list_filter = ('assessment_status', 'case_status', 'counseling', 'follow_up', 'referred')
    search_fields = ('user__username', 'updated_by__username', 'comments')
    date_hierarchy = 'date'
    readonly_fields = ('updated_at',)

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
