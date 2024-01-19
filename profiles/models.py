# profile/models.py
import uuid
from django.contrib.auth.models import User
from django.db import models
from wallets.models import Wallet

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=20)
#     address = models.CharField(max_length=200)

#     def __str__(self):
#         return self.user.username
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Customer - {self.first_name}"
    

class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    bvn = models.CharField(max_length=11)
    vendor_id = models.UUIDField(unique=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    virtual_account_number = models.CharField(max_length=20)
    bank = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    business_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Vendor - {self.business_name}"
