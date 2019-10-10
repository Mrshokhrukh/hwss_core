from django.contrib import admin
from .models import (
    ServiceAndTreatment, 
    ServiceAndTreatmentHistory, 
    Referral, 
    Substance, 
    Rescreening, 
    SubstanceRiskMeasurement
)

class ServiceAndTreatmentHistoryInline(admin.TabularInline):
    model = ServiceAndTreatmentHistory
    extra = 0
    readonly_fields = ('updated_by', 'updated_at', 'changes')


class RescreeningInline(admin.TabularInline):
    model = Rescreening
    extra = 0
    readonly_fields = ('user', 'submission_date', 'rescreening_count')


class ReferralInline(admin.TabularInline):
    model = Referral
    extra = 0
    readonly_fields = ('user', 'referred_by', 'referred_to', 'date', 'referral_status')


@admin.register(ServiceAndTreatment)
class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'assessment_status', 'case_status', 'counseling', 'referred')
    list_filter = ('assessment_status', 'case_status', 'counseling', 'referred')
    search_fields = ('user__username', 'comments')
    inlines = [ServiceAndTreatmentHistoryInline, RescreeningInline, ReferralInline]
    readonly_fields = ('updated_at',)


@admin.register(ServiceAndTreatmentHistory)
class ServiceAndTreatmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('service_and_treatment', 'updated_by', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('service_and_treatment__user__username', 'changes')
    readonly_fields = ('updated_at',)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by', 'referred_to_name', 'referral_status', 'date')
    list_filter = ('referral_status', 'date')
    search_fields = ('user__username', 'referred_to_name', 'referral_remarks')
    readonly_fields = ('date',)


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SubstanceRiskMeasurementInline(admin.TabularInline):
    model = SubstanceRiskMeasurement
    extra = 0
    readonly_fields = ('substance', 'measurement', 'risk_flag', 'total_score')


@admin.register(Rescreening)
class RescreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'submission_date', 'rescreening_count', 'rescreened')
    list_filter = ('rescreened', 'submission_date')
    search_fields = ('user__username',)
    readonly_fields = ('submission_date',)
    inlines = [SubstanceRiskMeasurementInline]


@admin.register(SubstanceRiskMeasurement)
class SubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ('substance', 'rescreening', 'measurement', 'risk_flag', 'total_score')
    list_filter = ('substance',)
    search_fields = ('rescreening__user__username', 'substance__name')
