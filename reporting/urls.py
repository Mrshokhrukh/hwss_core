from django.urls import path
from .views import orchestrate_reporting, populate_reporting_model_view

urlpatterns = [
    path('generate-report/', orchestrate_reporting, name='orchestrate_reporting'),
    path('build-reporting-data/', populate_reporting_model_view, name='populate_reporting_model_view'),
]
