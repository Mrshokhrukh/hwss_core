from django.urls import path
from .views import save_submission, MeasurementListView, MeasurementAssistListView, SubmissionListView

urlpatterns = [
    path('submit-screening/', save_submission, name='submit_screening'),
    path('get-measurement/', MeasurementListView.as_view(), name='measurement-list'),
    path('get-assist-measurement/', MeasurementAssistListView.as_view(), name='measurement-assist-list'),
    path('get-submission-data/', SubmissionListView.as_view(), name='submission-list'),
]
