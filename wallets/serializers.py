
# serializers.py
from rest_framework import serializers
from .models import Wallet, Transactions

class WalletAddMoneySerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class WalletRemoveMoneySerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    account_number = serializers.CharField(max_length=20)
    bank = serializers.CharField(max_length=20)
    account_name = serializers.CharField(max_length=20)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
