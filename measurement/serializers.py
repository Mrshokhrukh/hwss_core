# serializers.py
from rest_framework import serializers
from .models import Measurement, MeasurementAssist

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class MeasurementAssistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementAssist
        fields = '__all__'
