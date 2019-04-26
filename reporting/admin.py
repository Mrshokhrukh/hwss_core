from django.contrib import admin
from .models import Reporting, ReportingModel


class ReportingAdmin(admin.ModelAdmin):
    list_display = ['user', 'agency_code', 'agency_name', 'present_dzongkhag', 'present_gewog', 'present_village',
                    'user_code', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'referral_status', 'referral_remarks']
    search_fields = ['user__username', 'agency_code', 'agency_name', 'present_dzongkhag', 'present_gewog', 'present_village',
                     'user_code', 'assessment_status', 'case_status', 'counseling', 'follow_up', 'referral_status', 'referral_remarks']
    list_filter = ['assessment_status', 'case_status',
                   'counseling', 'referral_status']
    list_per_page = 20

class ReportingModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_agency', 'agency', 'service_and_treatment', 'referral', 'gad_score', 'gad_interpretation',
                    'phq_score', 'phq_interpretation', 'suicidal_score', 'suicidal_intepretation', 'ace_score', 'ace_interpretation',
                    'previous_diagnosis', 'alcoholic_measurement', 'alcoholic_flag', 'tobacco_measurement', 'tobacco_flag',
                    'cannabis_measurement', 'cannabis_flag', 'cocaine_measurement', 'cocaine_flag', 'amphetamine_measurement',
                    'amphetamine_flag', 'inhalants_measurement', 'inhalants_flag', 'sedatives_measurement', 'sedatives_flag',
                    'hallucinogens_measurement', 'hallucinogens_flag', 'opioids_measurement', 'opioids_flag', 'injection_measurement',
                    'injection_flag', 'other_measurement', 'other_flag', 'other_name', 'rescreened', 'rescreened_by',
                    'original_submission_date', 'rescreened_date']
    search_fields = ['user__username', 'user_agency__user__email', 'agency__agency_name', 'service_and_treatment__date',
                     'referral__date', 'gad_score', 'gad_interpretation', 'phq_score', 'phq_interpretation', 'suicidal_score',
                     'suicidal_intepretation', 'ace_score', 'ace_interpretation', 'previous_diagnosis', 'alcoholic_measurement',
                     'alcoholic_flag', 'tobacco_measurement', 'tobacco_flag', 'cannabis_measurement', 'cannabis_flag', 'cocaine_measurement',
                     'cocaine_flag', 'amphetamine_measurement', 'amphetamine_flag', 'inhalants_measurement', 'inhalants_flag',
                     'sedatives_measurement', 'sedatives_flag', 'hallucinogens_measurement', 'hallucinogens_flag', 'opioids_measurement',
                     'opioids_flag', 'injection_measurement', 'injection_flag', 'other_measurement', 'other_flag', 'other_name',
                     'rescreened', 'rescreened_by__username', 'original_submission_date', 'rescreened_date']
    list_filter = ['gad_score', 'phq_score', 'suicidal_score', 'ace_score', 'rescreened']
    list_per_page = 20


admin.site.register(ReportingModel, ReportingModelAdmin)
admin.site.register(Reporting, ReportingAdmin)
