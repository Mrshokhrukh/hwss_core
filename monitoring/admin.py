from django.contrib import admin
from .models import ServiceAndTreatment, Referral, Rescreening

class ServiceAndTreatmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'assessment_status', 'case_status', 'counseling']
    list_filter = ['assessment_status', 'case_status', 'counseling']
    search_fields = ['user__username', 'date', 'comments']

admin.site.register(ServiceAndTreatment, ServiceAndTreatmentAdmin)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'referred_to', 'referral_status']
    list_filter = ['referral_status']
    search_fields = ['user__username', 'referred_to', 'referred_to_name', 'referral_remarks']

admin.site.register(Referral, ReferralAdmin)

class RescreeningAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'submission_diagnosis']
    search_fields = ['user__username', 'submission_diagnosis']

admin.site.register(Rescreening, RescreeningAdmin)
