from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_event_screening, get_counselor_info, submit_case_screening, submit_event_screening, get_event_screenings, update_event_screening, EventBasedRecordViewSet, CaseBasedRecordViewSet

router = DefaultRouter()
router.register(r'event-records', EventBasedRecordViewSet, basename='event-records')
router.register(r'case-records', CaseBasedRecordViewSet, basename='case-records')

urlpatterns = [
    path('', include(router.urls)),
    path('create-event-screening/', create_event_screening, name='create_event_screening'),
    path('get-event-info/<str:counselor_name>/', get_counselor_info, name='get_counselor_info'),
    path('submit-case-screening/', submit_case_screening, name='submit_case_screening'),
    path('submit-event-screening/', submit_event_screening, name='submit_event_screening'),
    path('get-event-screenings/', get_event_screenings, name='get_event_screenings'),
    path('update-event-screening/', update_event_screening, name='update_event_screening'),
]
