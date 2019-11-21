from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReferralViewSet, ServiceAndTreatmentViewSet, get_notifications, list_final_submissions, mark_notification_as_read, process_rescreening,
    getReferralList, retrieve_final_submission, submit_rescreening,
    generateServiceAndTreatment, get_user_monitoring_details,
    update_service_and_treatment, update_referral_status, accept_referral, reject_referral
)

router = DefaultRouter()
router.register(r'service-and-treatment', ServiceAndTreatmentViewSet)
router.register(r'referrals', ReferralViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('final-submissions/', list_final_submissions,
         name='list_final_submissions'),
    path('final-submissions/<int:user_id>/retrieve/',
         retrieve_final_submission, name='retrieve_final_submission'),
    path('check-rescreening-flags/', process_rescreening,
         name='check_rescreening_flags'),
    path('generate-service-and-treatment/', generateServiceAndTreatment,
         name='generate_service_and_treatment'),
    path('get-referral-list/', getReferralList, name='get_referral_list'),
    path('submit-rescreening/', submit_rescreening, name='submit_rescreening'),
    path('get-user-monitoring-details/', get_user_monitoring_details,
         name='get_user_monitoring_details'),
    path('update-service-and-treatment/', update_service_and_treatment,
         name='update_service_and_treatment'),
    path('update-referral-status/', update_referral_status,
         name='update_referral_status'),
    path('accept-referral/', accept_referral, name='accept_referral'),
    path('reject-referral/', reject_referral, name='reject_referral'),
    path('get-notification/<int:user_id>/',
         get_notifications, name='get_notifications'),
    path('notifications/mark-as-read/', mark_notification_as_read,
         name='mark_notification_as_read'),
]
