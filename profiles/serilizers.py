# profile/serializers.py
from rest_framework import serializers
from .models import Customer, Vendor
from wallets.models import Wallet
from wallets.serializers import WalletSerializer

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['account_number', 'bvn', 'bank', 'business_name', 'business_phone_number', 'vendor_id', 'user', 'wallet']

    def create(self, validated_data):
        # Extract the wallet data from the validated data
        wallet_data = validated_data.pop('wallet', None)
        

        # Create the Vendor instance
        vendor = Vendor.objects.create(**validated_data)

        # If wallet data is provided, create or update the Wallet instance
        if wallet_data:
            wallet, created = Wallet.objects.update_or_create(user=vendor.user, defaults=wallet_data)
            vendor.wallet = wallet
            vendor.save()

        return vendor

class VendorEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['virtual_account_number', 'bank', 'business_name', 'business_phone_number']


# class VendorViewSerializer(serializers.ModelSerializer):
#     wallet = WalletSerializer()
#     class Meta:
#         model = Vendor
#         fields = ["__all__", wallet]
        
class VendorViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"


class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['account_number', 'bvn', 'first_name', 'last_name', 'phone_number', 'customer_id', 'user', 'wallet']

    def create(self, validated_data):
        # Extract the wallet data from the validated data
        wallet_data = validated_data.pop('wallet', None)
        

        # Create the Vendor instance
        vendor = Customer.objects.create(**validated_data)

        # If wallet data is provided, create or update the Wallet instance
        if wallet_data:
            wallet, created = Wallet.objects.update_or_create(user=vendor.user, defaults=wallet_data)
            vendor.wallet = wallet
            vendor.save()

        return vendor
    

class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
