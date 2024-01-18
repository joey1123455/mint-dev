# profile/serializers.py
from rest_framework import serializers
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_type', 'first_name', 'last_name', 'phone_number', 'address', ]
