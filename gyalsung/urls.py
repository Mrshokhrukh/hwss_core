from django.urls import include, path
from rest_framework.routers import DefaultRouter

from gyalsung.views import (
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

urlpatterns = [
    path("", include(router.urls)),
]
