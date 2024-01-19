from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
import os 
from squad import Squad
from dotenv import load_dotenv

from .serializers import WalletAddMoneySerializer

load_dotenv()

# Create your views here.

# load wallet
class LoadWalletAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    squad_obj = Squad(secret_key=os.getenv('SQUAD_KEY'))

    def post(self, request, *args, **kwargs):
        serializer = WalletAddMoneySerializer(data=request.data)
