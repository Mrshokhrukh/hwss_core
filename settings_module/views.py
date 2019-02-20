from rest_framework import generics
from rest_framework.response import Response
from .models import AppConfig, MenuItem
from .serializers import AppConfigSerializer, MenuItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.views import APIView


class AppConfigListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer


class MenuItemsAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]  # Adjust the permissions as needed
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        if self.request.user.is_authenticated:
            user_groups = self.request.user.groups.values_list('name', flat=True)
            queryset = queryset.filter(roles__name__in=user_groups).distinct()
        return queryset
