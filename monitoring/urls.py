from django.urls import path
from .views import process_rescreening,  getReferralList, submit_rescreening, generateServiceAndTreatment, get_user_monitoring_details

urlpatterns = [
    path('check-rescreening-flags/', process_rescreening, name='check_rescreening_flags'),
    path('generate-service-and-treatment/', generateServiceAndTreatment, name='generateServiceAndTreatment'),
    path('get-referral-list/', getReferralList, name='getReferralList'),
    path('submit-rescreening/', submit_rescreening, name='submit_rescreening'),
    path('get-user-monitoring-details/', get_user_monitoring_details, name='get_user_monitoring_details'),

]
