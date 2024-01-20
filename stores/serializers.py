from rest_framework import serializers
from .models import Products, Order

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'vendor', 'price', 'product_id', 'description', 'image']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'total_price', 'created_at', 'updated_at']