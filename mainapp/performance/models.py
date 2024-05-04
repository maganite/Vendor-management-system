from django.db import models
from vendor.models import Vendor

class Performance(models.Model):
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField
    quality_rating_avg = models.FloatField
    average_response_time = models.FloatField
    fulfillment_rate = models.FloatField