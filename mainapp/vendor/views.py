from django.shortcuts import render
from rest_framework import generics
from .models import Vendor
from .serializers import VendorsSerializers
from rest_framework.response import Response
from rest_framework import status
from purchase.models import PurchaseOrder, OrderStatus
from purchase.serializers import PurchaseSerializers
from datetime import datetime, timezone, timedelta
from performance.models import Performance
from performance.serializers import PerformanceSerializer
from django.shortcuts import get_object_or_404


class PerformanceApi(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = PerformanceSerializer

    def get_object(self, vendor_id):
        return get_object_or_404(Vendor, vendor_code=vendor_id)

    def get(self, request, *args, **kwargs):
        vendor_id = self.kwargs['vendor_code']
        vendor_object = self.get_object(vendor_id)
        performance_instance = Performance.objects.create(
            vendor = vendor_object,
            on_time_delivery_rate=vendor_object.on_time_delivery_rate,
            quality_rating_avg = vendor_object.quality_rating_avg,
            average_response_time = vendor_object.average_response_time,
            fulfillment_rate = vendor_object.fulfillment_rate
            )
        serializer = self.get_serializer(performance_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderApi(generics.UpdateAPIView):
    serializer_class = PurchaseSerializers

    def update_order_delivery(self, object):
        current_time = datetime.now()
        current_aware_time = current_time.astimezone(timezone.utc)
        object.order_date = current_aware_time
        object.delivery_date = current_aware_time + timedelta(days=7)
        object.status = OrderStatus.PENDING
        return object

    def patch(self, request, *args, **kwargs):
        self.po_number = self.kwargs['po_number']
        object = PurchaseOrder.objects.filter(po_number=self.po_number).first()
        if object is None:
            return Response({"message":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        if object.status == "completed":
            return Response({"message":"The order is already completed"})
        updated_object = self.update_order_delivery(object)
        serializer = self.get_serializer(updated_object, data=request.data, partial=True)
        if serializer.is_valid() == False:
            return Response({"message":"Enter corect datetime format"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorsListCreateApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorsSerializers
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid() == False:
            return Response({"Exists":"The vendor is already exists"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class VendorUpdatedeleteView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = VendorsSerializers
    queryset = Vendor.objects.all()

    def get_object(self, vendor_code):
        return Vendor.objects.filter(vendor_code=vendor_code).first()

    def put(self, request, *args, **kwargs):
        self.vendor_code = self.kwargs['vendor_code']
        partial = kwargs.pop('partial', False)
        instance = self.get_object(self.vendor_code)
        if instance is None:
            return Response({"message":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid() == False:
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
        

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.vendor_code = self.kwargs['vendor_code']
        object = self.get_object(self.vendor_code)
        if object is None:
            return Response({"message":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        self.vendor_code = self.kwargs['vendor_code']
        object = self.get_object(self.vendor_code)
        if object is None:
            return Response({"message":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response({},status=status.HTTP_204_NO_CONTENT)