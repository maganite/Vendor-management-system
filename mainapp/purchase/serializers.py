from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        depth = 1