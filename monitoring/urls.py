from django.urls import path
from .views import process_rescreening,  getReferralList, submit_rescreening, generateServiceAndTreatment, get_user_monitoring_details, update_service_and_treatment, update_referral_status, accept_referral, reject_referral

urlpatterns = [
    path('check-rescreening-flags/', process_rescreening, name='check_rescreening_flags'),
    path('generate-service-and-treatment/', generateServiceAndTreatment, name='generateServiceAndTreatment'),
    path('get-referral-list/', getReferralList, name='getReferralList'),
    path('submit-rescreening/', submit_rescreening, name='submit_rescreening'),
    path('get-user-monitoring-details/', get_user_monitoring_details, name='get_user_monitoring_details'),
    path('update-service-and-treatment/', update_service_and_treatment, name='update_service_and_treatment'),
    path('update-referral-status/', update_referral_status, name='update_referral_status'),
    path('accept-referral/', accept_referral, name='accept_referral'),
    path('reject-referral/', reject_referral, name='reject_referral'),

]
