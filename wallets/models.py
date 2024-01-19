import uuid
from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=4) 
    limit_level = models.PositiveIntegerField(default=100000) 
    wallet_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Add a UUID wallet ID field
    account_number = models.CharField(max_length=20)  # Add an account number field
    bank = models.CharField(max_length=20)
    bvn = models.CharField(max_length=11)  # Add a BVN field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wallet - {self.wallet_id} ({self.user.username})"
