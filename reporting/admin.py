from django.contrib import admin
from .models import Reporting, UserArchive


class ReportingAdmin(admin.ModelAdmin):
    list_display = ['user', 'agency_code', 'agency_name', 'present_dzongkhag', 'present_gewog', 'present_village',
                    'user_code', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'referral_status', 'referral_remarks']
    search_fields = ['user__username', 'agency_code', 'agency_name', 'present_dzongkhag', 'present_gewog', 'present_village',
                     'user_code', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'referral_status', 'referral_remarks']
    list_filter = ['assessment_status', 'case_status',
                   'counseling', 'referral_status']
    list_per_page = 20


class UserArchiveAdmin(admin.ModelAdmin):
    list_display = ['identity_number', 'first_name', 'last_name', 'agency_code', 'agency_name', 'present_dzongkhag',
                    'present_gewog', 'present_village', 'assessment_status', 'case_status', 'counseling', 'referral_status', 'referral_remarks']
    search_fields = ['identity_number', 'first_name', 'last_name', 'agency_code', 'agency_name', 'present_dzongkhag',
                     'present_gewog', 'present_village', 'assessment_status', 'case_status', 'counseling', 'referral_status', 'referral_remarks']
    list_filter = ['assessment_status', 'case_status',
                   'counseling', 'referral_status']
    list_per_page = 20


admin.site.register(Reporting, ReportingAdmin)
admin.site.register(UserArchive, UserArchiveAdmin)
