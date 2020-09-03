from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from access.models import CustomUser
from gyalsung.serializers import GyalsungCounselorUserSerializer


class GyalsungCounselorUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_counselors()
        qs.select_related(
            "active_agency",
        )
        return qs


class GyalsungReassessmentTeamUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        return qs
