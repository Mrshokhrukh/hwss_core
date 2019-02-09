from rest_framework import serializers
from .models import AppConfig

class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = '__all__'
