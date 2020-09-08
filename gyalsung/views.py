from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from access.models import CustomUser
from gyalsung.serializers import (
    GyalsungCounselorUserSerializer,
    GyalsungFitUnfitUserSerializer,
)


class GyalsungCounselorUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_counselors()
        qs.select_related(
            "active_agency",
        )
        return qs


class GyalsungReassessmentTeamUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        return qs


class GyalsungReassessmentMonitoringUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status__in=["fit", "unfit"])
        return qs


class GyalsungReassessmentFitUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status="fit")
        return qs


class GyalsungReassessmentUnfitUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status="unfit")
        return qs
