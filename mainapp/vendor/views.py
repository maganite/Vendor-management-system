from django.shortcuts import render
from rest_framework import generics
from .models import Vendor
from .serializers import VendorsSerializers
from rest_framework.response import Response
from rest_framework import status

class VendorsListCreateApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorsSerializers

class VendorUpdatedeleteView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorsSerializers
    lookup_field = 'vendor_code'

    def get_queryset(self):
        queryset = self.queryset
        # print(self.kwargs)
        # print(self.request.data)
        # print(self.args)
        queryset = queryset.filter(vendor_code=self.kwargs[self.lookup_field])
        return queryset