from django.urls import path
from .views import (
    orchestrate_reporting, 
    populate_reporting_model_view, 
    get_reporting_model_data, healthz, 
    generate_counselor_report_encrypted_xls
)

urlpatterns = [
    path('generate-report/', orchestrate_reporting, name='orchestrate_reporting'),
    path('build-reporting-data/', populate_reporting_model_view, name='populate_reporting_model_view'),
    path('get-reporting-model-data/', get_reporting_model_data, name='get_reporting_model_data'),
    path('generate-counselor-report-encrypted-xls/', generate_counselor_report_encrypted_xls, name='generate_counselor_report_encrypted_xls'),
    path('healthz', healthz, name='healthz'),
]
