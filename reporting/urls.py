from django.urls import path
from .views import orchestrate_reporting

urlpatterns = [
    path('generate-report/', orchestrate_reporting, name='orchestrate_reporting'),
]
