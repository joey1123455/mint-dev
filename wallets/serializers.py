
# serializers.py
from rest_framework import serializers
from .models import Wallet

class WalletAddMoneySerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'pin', 'limit_level', 'wallet_id', 'account_number', 'bank', 'bvn', 'user']
