from django.urls import path

from reporting.views import (
    get_reporting_model_data,
    healthz,
    orchestrate_reporting,
    populate_reporting_model_view,
)

urlpatterns = [
    path("generate-report/", orchestrate_reporting, name="orchestrate_reporting"),
    path(
        "build-reporting-data/",
        populate_reporting_model_view,
        name="populate_reporting_model_view",
    ),
    path(
        "get-reporting-model-data/",
        get_reporting_model_data,
        name="get_reporting_model_data",
    ),
    path("healthz", healthz, name="healthz"),
]
