from rest_framework import serializers
from .models import Vendor


class VendorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
