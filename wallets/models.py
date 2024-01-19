import uuid
from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=4)  # Add a PIN field for simplicity, adjust as needed
    limit_level = models.PositiveIntegerField(default=1)  # Add a limit level field
    wallet_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Add a UUID wallet ID field
    account_number = models.CharField(max_length=20, unique=True)  # Add an account number field
    bvn = models.CharField(max_length=11, unique=True)  # Add a BVN field
    # Add other wallet-related fields as needed

    def __str__(self):
        return f"Wallet - {self.wallet_id} ({self.user.username})"
