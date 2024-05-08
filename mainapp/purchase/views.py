from django.shortcuts import render
from rest_framework import generics
from .models import PurchaseOrder, OrderStatus
from .serializers import PurchaseSerializers
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from vendor.models import Vendor
from vendor.serializers import VendorsSerializers

class RatingApi(generics.UpdateAPIView):
    serializer_class = PurchaseSerializers

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        self.po_number = self.kwargs['po_number']
        object = PurchaseOrder.objects.filter(po_number=self.po_number).first()
        if object is None:
            return Response({"message":"Purchase order not found"},status=status.HTTP_404_NOT_FOUND)
        if object.status == "completed":
            print("$$$$$$$$$$$$$$$$$$$$$$$4")
            Vendor.qualityrating(object, request_data)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            object.quality_rating = request_data.get('quality_rating')
            serializer = self.get_serializer(object, data=request.data, partial=True)
            if serializer.is_valid() == False:
                return Response({"message":"enter the correct ratings"})
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message":"the order is yet to be delivered"})
    

class DeliveryApi(generics.UpdateAPIView):
    serializer_class = PurchaseSerializers

    def deliverydate(self, object):
        current_time = datetime.now()
        current_aware_time = current_time.astimezone(timezone.utc)
        real_delivery_date = current_aware_time
        if object.status == "completed":
            return object
        Vendor.ontimedelivery(object, real_delivery_date)
        object.delivery_date = real_delivery_date
        return object

    def patch(self, request, *args, **kwargs):
        self.po_number = self.kwargs['po_number']
        object = PurchaseOrder.objects.filter(po_number=self.po_number).first()
        if object is None:
            return Response({"message":"purchase order not found"},status=status.HTTP_404_NOT_FOUND)
        updated_object = self.deliverydate(object)
        if updated_object.status == "completed":
            return Response({"message":"The order is already completed"})
        updated_object.status = OrderStatus.COMPLETED
        serializer = self.get_serializer(updated_object, data=request.data, partial=True)
        if serializer.is_valid() == False:
            return Response({"message":"Enter corect datetime format"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AcknowledgeApi(generics.UpdateAPIView):
    serializer_class = PurchaseSerializers

    def acknowledgetime(self, object):
        current_time = datetime.now()
        current_aware_time = current_time.astimezone(timezone.utc)
        object.acknowledgment_date = current_aware_time
        return object

    def patch(self, request, *args, **kwargs):
        self.po_number = self.kwargs['po_number']
        object = PurchaseOrder.objects.filter(po_number=self.po_number).first()
        if object is None:
            return Response({"message":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        if object.status == "completed":
            return Response({"message":"The order is already completed"})
        updated_object = self.acknowledgetime(object)
        serializer = self.get_serializer(updated_object, data=request.data, partial=True)
        if serializer.is_valid() == False:
            return Response({"message":"Enter corect datetime format"})
        serializer.save()
        Vendor.responsetime(object)
        return Response(serializer.data, status=status.HTTP_200_OK)




class PurchaseListCreateApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializers
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid() == False:
            return Response({"Exists":"The order is already exists"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class PurchaseUpdatedeleteView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializers
    lookup_field = 'po_number'

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(po_number=self.kwargs[self.lookup_field])
        return queryset