from django.contrib import admin
from .models import ServiceAndTreatment, ServiceAndTreatmentHistory, Referral, Substance, Rescreening, SubstanceRiskMeasurement

@admin.register(ServiceAndTreatment)
class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'assessment_status', 'case_status', 'counseling', 'follow_up')
    list_filter = ('assessment_status', 'case_status', 'counseling')
    search_fields = ('user__username', 'comments')

@admin.register(ServiceAndTreatmentHistory)
class ServiceAndTreatmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('service_and_treatment', 'updated_by', 'updated_at')
    search_fields = ('service_and_treatment__user__username', 'changes')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by', 'date', 'referred_to_name', 'referral_status')
    list_filter = ('referral_status',)
    search_fields = ('user__username', 'referred_by__username', 'referred_to_name')

@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Rescreening)
class RescreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'submission_date', 'rescreened')
    list_filter = ('rescreened',)
    search_fields = ('user__username',)

@admin.register(SubstanceRiskMeasurement)
class SubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'rescreening', 'measurement', 'risk_flag', 'total_score')
    search_fields = ('substance__name', 'rescreening__user__username')
