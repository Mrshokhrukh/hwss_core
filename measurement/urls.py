from django.urls import path

from measurement.views import (
    CombinedListView,
    MeasurementAssistListView,
    MeasurementListView,
    SubmissionListView,
    fetch_school_env_entries,
    get_user_diagnosis,
    main_composer,
    save_submission,
)

urlpatterns = [
    path("submit-screening/", save_submission, name="submit_screening"),
    path("get-measurement/", MeasurementListView.as_view(), name="measurement-list"),
    path(
        "get-assist-measurement/",
        MeasurementAssistListView.as_view(),
        name="measurement-assist-list",
    ),
    path("get-submission-data/", SubmissionListView.as_view(), name="submission-list"),
    path("get-measurement-data/", CombinedListView.as_view(), name="measurement-list"),
    path("get-sud-data/", main_composer, name="main_composer"),
    path(
        "get-school-env-data/",
        fetch_school_env_entries,
        name="fetch_school_env_entries",
    ),
    path("diagnosis/<int:user_id>/", get_user_diagnosis, name="get_user_diagnosis"),
]
