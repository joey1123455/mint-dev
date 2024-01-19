# profile/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['user_type', 'first_name', 'last_name', 'phone_number', 'address', ]

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Customer
        fields = ['user', 'customer_id', 'wallet', 'first_name', 'last_name', 'phone_number', 'account_number', 'bvn',]

    def create(self, validated_data):
        user = validated_data.pop('user')
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
