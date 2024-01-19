import uuid
from django.db import models
from profiles.models import Vendor
from django.contrib.auth.models import User

class Products(models.Model):
    name = models.CharField(max_length=200)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    price = models.IntegerField()
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    