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

from .serializers import WalletAddMoneySerializer, TransactionsSerializer, WalletSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Transactions, Wallet


load_dotenv()

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
            amount = serializer.validated_data['amount'] * 100
            id = uuid.uuid4()
            wallet = Wallet.objects.get(id=wallet_id)
            transaction = Transactions.objects.create(
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
                "amount": amount,
                "currency":"NGN",
                "initiate_type": "inline",
                "transaction_ref": str(id),
                "email": email,
                "payment_channels": ['card', 'bank' , 'ussd','transfer']
            }
            res = self.squad_obj.payments.initiate_transaction(data)
            if res["status"] != 200:
                return Response({'error': res["message"]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'payment link': res["data"]["checkout_url"]}, status=status.HTTP_204_NO_CONTENT)
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


