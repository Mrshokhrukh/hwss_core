from django.urls import path
from .views import create_event_screening, get_counselor_info

urlpatterns = [
    path('create-event-screening/', create_event_screening, name='create_event_screening'),
    path('get-event-info/<str:counselor_name>/', get_counselor_info, name='get_counselor_info'),
]
