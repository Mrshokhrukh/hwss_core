from django.urls import path
from .views import process_rescreening, getServiceAndTreatmentList, getReferralList

urlpatterns = [
    path('check-rescreening-flags/', process_rescreening, name='check_rescreening_flags'),
    path('get-service-and-treatment/', getServiceAndTreatmentList, name='getServiceAndTreatmentList'),
    path('get-referral-list/', getReferralList, name='getReferralList'),
]
