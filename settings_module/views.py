from rest_framework import generics
from rest_framework.response import Response
from .models import AppConfig
from .serializers import AppConfigSerializer

class AppConfigListView(generics.ListAPIView):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
