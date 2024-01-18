# profile/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
    

class Customer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # Add other customer-specific fields here

    def __str__(self):
        return f"Customer - {self.profile.user.username}"
    

class Vendor(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Add other vendor-specific fields here

    def __str__(self):
        return f"Vendor - {self.profile.user.username}"
