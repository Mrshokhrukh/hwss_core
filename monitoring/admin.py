from django.contrib import admin
from .models import ServiceAndTreatment, Referral, Substance, Rescreening, SubstanceRiskMeasurement


class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'assessment_status',
                    'case_status', 'counseling']
    list_filter = ['assessment_status', 'case_status', 'counseling']
    search_fields = ['user__username', 'date', 'comments']


admin.site.register(ServiceAndTreatment, ServiceAndTreatmentAdmin)


class ReferralAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'referred_to', 'referral_status']
    list_filter = ['referral_status']
    search_fields = ['user__username', 'referred_to',
                     'referred_to_name', 'referral_remarks']


admin.site.register(Referral, ReferralAdmin)


class SubstanceAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Substance, SubstanceAdmin)


class SubstanceRiskMeasurementInline(admin.TabularInline):
    model = SubstanceRiskMeasurement
    extra = 1


class RescreeningAdmin(admin.ModelAdmin):
    list_display = ['user', 'submission_date', 'rescreened']
    inlines = [SubstanceRiskMeasurementInline]


admin.site.register(Rescreening, RescreeningAdmin)


class SubstanceRiskMeasurementAdmin(admin.ModelAdmin):
    list_display = ['substance', 'rescreening', 'measurement', 'risk_flag']


admin.site.register(SubstanceRiskMeasurement, SubstanceRiskMeasurementAdmin)
