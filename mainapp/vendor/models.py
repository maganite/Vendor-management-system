from django.db import models
from datetime import datetime, timedelta

class Vendor(models.Model):
    Response_list = []
    ontime_count = []
    completed_time = []
    full_fillment_rate = []
    rating = []
    
    vendor_code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    contact_details = models.TextField(unique=True)
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(blank=True, default=0.0)
    quality_rating_avg = models.FloatField(blank=True, default=0.0)
    average_response_time = models.FloatField(blank=True, default=0.0)
    fulfillment_rate = models.FloatField(blank=True, default=0.0)

    def __str__(self) -> str:
        return f"Name-{self.name}, Vendor_code-{self.vendor_code}"
    
    def responsetime(self):
        start_time = self.issue_date
        end_time = self.acknowledgment_date

        time_difference = end_time - start_time
        Vendor.Response_list.append(time_difference)

        total_delta = sum(Vendor.Response_list, timedelta(0))
        average_delta = total_delta / len(Vendor.Response_list)

        total_seconds = average_delta.total_seconds()   
        if total_seconds >= 60 * 60:
            formatted_timedelta = total_seconds / (60 * 60) 
            unit = "hours"
        elif total_seconds >= 60: 
            formatted_timedelta = total_seconds / 60 
            unit = "minutes"
        else:
            formatted_timedelta = total_seconds
            unit = "seconds"

        print(f"Formatted timedelta: {formatted_timedelta} {unit}")
        vendor_id = self.vendor_id
        vendor_obj = Vendor.objects.filter(vendor_code=vendor_id).first()
        vendor_obj.average_response_time = formatted_timedelta
        vendor_obj.save()
        
    def ontimedelivery(self, real_delivery_date):
        print(self.delivery_date)
        Vendor.completed_time.append(self.delivery_date)
        if real_delivery_date <= self.delivery_date:
            print(real_delivery_date, self.delivery_date)
            Vendor.ontime_count.append(real_delivery_date)
        on_time_delivery_data = float(len(Vendor.ontime_count)/len(Vendor.completed_time))
        print(on_time_delivery_data)
        print(Vendor.completed_time, Vendor.ontime_count)
        vendor_id = self.vendor_id
        vendor_obj = Vendor.objects.filter(vendor_code=vendor_id).first()
        vendor_obj.on_time_delivery_rate = on_time_delivery_data
        vendor_obj.save()

    def fullfillmentrate(self):
        pass

    def qualityrating(self, request_data):
        Vendor.rating.append(request_data.get('quality_rating'))
        print(Vendor.rating)
        total_rating = sum(Vendor.rating)
        print(total_rating)
        average_rating = total_rating / len(Vendor.rating)
        vendor_obj = Vendor.objects.filter(vendor_code = self.vendor_id).first()
        vendor_obj.quality_rating_avg = average_rating
        vendor_obj.save()
