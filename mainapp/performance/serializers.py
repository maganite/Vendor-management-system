from rest_framework import serializers
from .models import Performance


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        exclude = ('date', 'id', 'vendor')
