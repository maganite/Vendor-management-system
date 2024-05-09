from django.db import models
from datetime import datetime, timedelta


class Vendor(models.Model):
    vendor_code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    contact_details = models.TextField(unique=True)
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(blank=True, default=0.0)
    quality_rating_avg = models.FloatField(blank=True, default=0.0)
    average_response_time = models.FloatField(blank=True, default=0.0)
    fulfillment_rate = models.FloatField(blank=True, default=0.0)
    ontime_deliver_order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Name-{self.name}, Vendor_code-{self.vendor_code}"

    def responsetime(self):
        from purchase.models import PurchaseOrder
        start_time = self.issue_date
        end_time = self.acknowledgment_date

        time_difference = end_time - start_time
        seconds_difference = time_difference.total_seconds()
        total_order = PurchaseOrder.objects.filter(
            vendor_id=self.vendor_id).count()
        vendor_obj = Vendor.objects.filter(vendor_code=self.vendor_id).first()
        new_sum = total_order*vendor_obj.average_response_time + seconds_difference
        new_average = new_sum/total_order
        vendor_obj.average_response_time = new_average
        vendor_obj.save()

    def ontimedelivery(self):
        from purchase.models import PurchaseOrder
        vendor_obj = Vendor.objects.filter(vendor_code=self.vendor_id).first()
        on_time_deliveries = vendor_obj.ontime_deliver_order
        total_completed_order = PurchaseOrder.objects.filter(
            vendor_id=self.vendor_id).filter(status="completed").count()
        req_on_time_delivery_rate = on_time_deliveries/total_completed_order
        vendor_obj.on_time_delivery_rate = req_on_time_delivery_rate
        vendor_obj.save()

    def fullfillmentrate(self):
        from purchase.models import PurchaseOrder
        completed_order = PurchaseOrder.objects.filter(
            vendor_id=self.vendor_id).filter(status="completed").count()
        total_issued_order = PurchaseOrder.objects.filter(
            vendor_id=self.vendor_id).count()
        req_fullfilment_rate = completed_order/total_issued_order
        vendor_obj = Vendor.objects.filter(vendor_code=self.vendor_id).first()
        vendor_obj.fulfillment_rate = req_fullfilment_rate
        vendor_obj.save()

    def qualityrating(self, request_data):
        from purchase.models import PurchaseOrder
        total_order = PurchaseOrder.objects.filter(
            vendor_id=self.vendor_id).count()
        vendor_obj = Vendor.objects.filter(vendor_code=self.vendor_id).first()
        new_sum = total_order*vendor_obj.quality_rating_avg + \
            request_data.get('quality_rating')
        print(new_sum)
        print(total_order)
        new_average = new_sum/(total_order)
        print(new_average)
        vendor_obj.quality_rating_avg = new_average
        vendor_obj.save()
