from rest_framework import generics
from rest_framework.response import Response
from .models import AppConfig
from .serializers import AppConfigSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions




class AppConfigListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
