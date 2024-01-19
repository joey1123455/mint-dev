# profile/views.py
from django.forms import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from .models import Profile
from .serilizers import  CustomerSerializer
from rest_framework.response import Response
from .models import Customer
from wallets.models import Wallet

# class UserProfileView(generics.RetrieveUpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return Profile.objects.get(user=self.request.user)

class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['user'] = request.user.id
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        serialized_data = serializer.validated_data

        user_wallet = Wallet.objects.create(
            account_number = serialized_data["account_number"],
            bvn = serialized_data["bvn"],
        )
        request.data['wallet'] = user_wallet.wallet_id
        
        
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()