from django.contrib import admin
from .models import ServiceAndTreatment, ServiceAndTreatmentHistory, Referral, Substance, Rescreening, SubstanceRiskMeasurement, FinalUserSubmission

@admin.register(ServiceAndTreatment)
class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'updated_by', 'updated_at')
    list_filter = ('assessment_status', 'case_status', 'counseling', 'follow_up', 'updated_by', 'updated_at')
    search_fields = ('user__username', 'comments')
    date_hierarchy = 'updated_at'


@admin.register(ServiceAndTreatmentHistory)
class ServiceAndTreatmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('service_and_treatment', 'updated_by', 'updated_at')
    list_filter = ('updated_by', 'updated_at')
    search_fields = ('service_and_treatment__user__username', 'changes')
    date_hierarchy = 'updated_at'


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by', 'referred_to_name', 'referral_status', 'date')
    list_filter = ('referral_status', 'date')
    search_fields = ('user__username', 'referred_to_name', 'referral_remarks')
    date_hierarchy = 'date'


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Rescreening)
class RescreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'phq_score', 'gad_score', 'ace_score', 'rescreened', 'rescreening_count', 'submission_date')
    list_filter = ('rescreened', 'submission_date')
    search_fields = ('user__username', 'phq_interpretation', 'gad_interpretation', 'ace_interpretation')
    date_hierarchy = 'submission_date'


@admin.register(SubstanceRiskMeasurement)
class SubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'rescreening', 'measurement', 'risk_flag', 'total_score')
    list_filter = ('substance', 'rescreening__user__username')
    search_fields = ('substance__name', 'rescreening__user__username', 'risk_flag')


@admin.register(FinalUserSubmission)
class FinalUserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'phq_score', 'gad_score', 'ace_score', 'assist_score', 'rescreened', 'rescreening_count', 'submission_date')
    list_filter = ('rescreened', 'submission_date')
    search_fields = ('user__username', 'phq_interpretation', 'gad_interpretation', 'ace_interpretation', 'assist_interpretation')
    date_hierarchy = 'submission_date'
