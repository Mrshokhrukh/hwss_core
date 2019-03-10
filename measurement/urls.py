from django.urls import path
from .views import save_submission

urlpatterns = [
    path('submit-screening/', save_submission, name='submit_screening'),
]
