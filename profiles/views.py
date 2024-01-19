# profile/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.authentication import TokenAuthentication

# myapp/views.py
from rest_framework import status
from rest_framework.views import APIView
from .serilizers import VendorCreateSerializer, VendorEditSerializer, VendorViewSerializer
from squad import Squad
from dotenv import load_dotenv
import os
import uuid
from wallets.models import Wallet
from .models import Vendor

# Load variables from .env file
load_dotenv()

class VendorCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    squad_obj = Squad(secret_key=os.getenv('SQUAD_KEY'))

    def post(self, request, *args, **kwargs):
            
            wallet_data = {
                'bvn': request.data.get('bvn', None),
                'account_number': request.data.get('account_number', None),
                'user': request.user,
            }
            

            # wallet, created = Wallet.objects.get_or_create(**wallet_data)

            # Update request data with Wallet instance (not just ID)
            request.data['user'] = request.user.id
            vendor_id = uuid.uuid4()
            request.data['vendor_id'] = vendor_id
            print(request.data)

            serializer = VendorCreateSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError as e:
                return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data = serializer.validated_data
            data = {
                'beneficiary_account': serialized_data['account_number'],
                'bvn': serialized_data['bvn'],
                'customer_identifier': str(serialized_data['vendor_id']),
                'business_name': serialized_data['business_name'],
                'mobile_num': serialized_data['business_phone_number'],
            }

            res = self.squad_obj.virtual_accounts.create_business_virtual_account(data)
            if res["status"] != 200:
                return Response({'error': res["message"]}, status=status.HTTP_400_BAD_REQUEST)

            serializer.validated_data["virtual_account_number"] = res["data"]["virtual_account_number"]
            serializer.validated_data["wallet"] = wallet_data
            # serializer.validated_data["wallet"] = wallet.wallet_id
            serializer.save()

            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
    

class VendorListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve all vendors
        vendors = Vendor.objects.all()

        # Serialize the vendor data
        serializer = VendorViewSerializer(vendors, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class VendorDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(vendor_id=vendor_id)
        serializer = VendorViewSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
