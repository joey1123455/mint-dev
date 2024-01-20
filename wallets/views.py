from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
import os 
import uuid
from rest_framework import status
from squad import Squad
from dotenv import load_dotenv
import hashlib
from django.utils import timezone

from .serializers import WalletAddMoneySerializer, TransactionsSerializer, WalletSerializer, WalletRemoveMoneySerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Transactions, Wallet


load_dotenv()

bank_codes = {
    "Sterling Bank": "000001",
    "Keystone Bank": "000002",
    "FCMB": "000003",
    "United Bank for Africa": "000004",
    "Diamond Bank": "000005",
    "JAIZ Bank": "000006",
    "Fidelity Bank": "000007",
    "Polaris Bank": "000008",
    "Citi Bank": "000009",
    "Ecobank Bank": "000010",
    "Unity Bank": "000011",
    "StanbicIBTC Bank": "000012",
    "GTBank Plc": "000013",
    "Access Bank": "000014",
    "Zenith Bank Plc": "000015",
    "First Bank of Nigeria": "000016",
    "Wema Bank": "000017",
}

# Create your views here.

# load wallet
class LoadWalletAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    squad_obj = Squad(secret_key=os.getenv('SQUAD_KEY'))

    def post(self, request, *args, **kwargs):
        serializer = WalletAddMoneySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            wallet_id = serializer.validated_data['wallet_id']
            amount = serializer.validated_data['amount']
            amount_to_send = serializer.validated_data['amount'] * 100
            id = uuid.uuid4()
            wallet = Wallet.objects.get(id=wallet_id)
            Transactions.objects.create(
                wallet_id=wallet_id, 
                amount=amount, 
                previous_balance=wallet.balance,
                new_balance=wallet.balance + amount,
                status='pending',
                transaction_id=id,
                type='load wallet',
                created_at=timezone.now()
                )
            email = request.user.email
            data = {
                "amount": amount_to_send,
                "currency":"NGN",
                "initiate_type": "inline",
                "transaction_ref": str(id),
                "email": email,
                "payment_channels": ['card', 'bank' , 'ussd','transfer'],
                "metadata": {"wallet_id": str(wallet_id)}
            }
            res = self.squad_obj.payments.initiate_transaction(data)
            if res["status"] != 200:
                return Response({'error': res["message"]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'payment_link': res["data"]}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        # Process the incoming webhook data
        body = request.body.decode('utf-8')

        # Validate the event using the secret key
        secret = os.getenv('SQUAD_KEY')
        received_hash = request.headers.get('X-Squad-Encrypted-Body', '').upper()
        calculated_hash = hashlib.sha512(secret.encode('utf-8') + body.encode('utf-8')).hexdigest().upper()

        if received_hash == calculated_hash:
            # Trust the event came from Squad and process accordingly
            # Add your webhook processing logic here
            return HttpResponse(status=200)


class WithdrawWalletAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    squad_obj = Squad(secret_key=os.getenv('SQUAD_KEY'))

    def post(self, request, *args, **kwargs):
        serializer = WalletRemoveMoneySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            wallet_id = serializer.validated_data['wallet_id']
            amount_to_send = serializer.validated_data['amount'] * 100
            name = serializer.validated_data["account_name"]
            code = bank_codes.get(serializer.validated_data['bank'])
            no = serializer.validated_data["account_number"]


            amount = serializer.validated_data['amount']
            id = uuid.uuid4()
            wallet = Wallet.objects.get(id=wallet_id)
            Transactions.objects.create(
                wallet_id=wallet_id, 
                amount=amount, 
                previous_balance=wallet.balance,
                new_balance=wallet.balance - amount,
                status='pending',
                transaction_id=id,
                type='withdraw wallet',
                created_at=timezone.now()
                )
            
            data = {
                "amount": amount_to_send,
                "bank_code":code,
                "account_number": no,
                "transaction_reference": "SB96V618PP_" +str(id),
                "account_name": name,
                "currency_id": "NGN",
                "remark": str(wallet_id)
            }
            res = self.squad_obj.transfer.fund_transfer(data)
            if res["status"] != 200:
                return Response({'error': res["message"]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'res': res["data"]}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


