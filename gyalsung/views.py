from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from access.models import CustomUser
from gyalsung.serializers import GyalsungCounselorUserSerializer

# Create your views here.


class GyalsungCounselorUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.for_gyalsung_counselors()


class GyalsungReassessmentTeamUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return CustomUser.objects.for_gyalsung_reassessment_team()
