from django.contrib.auth.models import Group
from rest_framework import serializers

from settings_module.models import AppConfig, MenuItem


class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            base_url = f"{request.scheme}://{request.get_host()}"
            for field in data:
                if isinstance(data[field], str) and data[field].startswith("/media/"):
                    data[field] = f"{base_url}/api/core{data[field]}"
        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class MenuItemSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ("name", "route", "icon_class", "roles")
