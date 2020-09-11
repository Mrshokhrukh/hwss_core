from django.urls import include, path
from rest_framework.routers import DefaultRouter

from gyalsung.views import (
    GyalsungCounselorUserViewSet,
    GyalsungReassessmentFitUserViewSet,
    GyalsungReassessmentMonitoringUserViewSet,
    GyalsungReassessmentTeamUserViewSet,
    GyalsungReassessmentUnfitUserViewSet,
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
    r"reassessment-monitoring",
    GyalsungReassessmentMonitoringUserViewSet,
    basename="reassessment-monitoring",
)
router.register(
    r"reassessment-fit-candidates",
    GyalsungReassessmentFitUserViewSet,
    basename="reassessment-fit-users",
)
router.register(
    r"reassessment-unfit-candidates",
    GyalsungReassessmentUnfitUserViewSet,
    basename="reassessment-unfit-users",
)

urlpatterns = [
    path("", include(router.urls)),
]
