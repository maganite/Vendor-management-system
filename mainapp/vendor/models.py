from django.db import models

class Vendor(models.Model):
    vendor_code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    contact_details = models.TextField(unique=True)
    address = models.TextField
    on_time_delivery_rate = models.FloatField
    quality_rating_avg = models.FloatField
    average_response_time = models.FloatField
    fulfillment_rate = models.FloatField
