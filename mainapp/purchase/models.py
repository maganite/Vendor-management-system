from django.db import models
from vendor.models import Vendor


class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True, max_length=20)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, blank=True)
    quality_rating = models.FloatField(blank=True, default=0.0)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Name-{self.vendor.name}, po_number-{self.po_number}"
