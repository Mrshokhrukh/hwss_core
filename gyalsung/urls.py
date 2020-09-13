from django.urls import include, path
from rest_framework.routers import DefaultRouter

from gyalsung.views import (
    GyalsungAssessmentViewSet,
    GyalsungCounselorUserViewSet,
    GyalsungReassessmentTeamUserViewSet,
)

router = DefaultRouter()
router.register(
    r"counselor-users", GyalsungCounselorUserViewSet, basename="counselor-users"
)
router.register(
    r"reassessment-users",
    GyalsungReassessmentTeamUserViewSet,
    basename="reassessment-users",
)
router.register(
    r"assessments", GyalsungAssessmentViewSet, basename="gyalsung-assessments"
)

urlpatterns = [
    path("", include(router.urls)),
]
