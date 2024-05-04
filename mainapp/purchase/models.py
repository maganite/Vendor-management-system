from django.db import models
from vendor.models import Vendor

class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True, max_length=20)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField
    items = models.JSONField
    quantity = models.IntegerField
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField
    acknowledgment_date = models.DateTimeField(null=True)
