from django.urls import path
from .views import save_submission, MeasurementListView, MeasurementAssistListView, SubmissionListView, CombinedListView

urlpatterns = [
    path('submit-screening/', save_submission, name='submit_screening'),
    path('get-measurement/', MeasurementListView.as_view(), name='measurement-list'),
    path('get-assist-measurement/', MeasurementAssistListView.as_view(), name='measurement-assist-list'),
    path('get-submission-data/', SubmissionListView.as_view(), name='submission-list'),
    path('get-measurement-data/', CombinedListView.as_view(), name='measurement-list'),
]
