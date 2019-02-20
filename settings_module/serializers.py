from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import AppConfig, MenuItem

class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class MenuItemSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ('name', 'route', 'icon_class', 'roles')
