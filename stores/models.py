import uuid
from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    