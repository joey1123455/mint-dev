from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Products, Order
from profiles.models import Vendor
from .serializers import ProductsSerializer, OrderSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVendorUser
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication

# Create your views here.
# @permission_classes([IsAuthenticated])

class AddProduct(APIView):
    permission_classes = [IsAuthenticated, IsVendorUser]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        is_vendor = Vendor.objects.filter(user=user).exists()

        if is_vendor:
            serializer.save()
        else:
            raise PermissionDenied("Only vendors can create products.")

    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductsView(APIView):
    def get(self, request, id=None):
        if id:
            product = Products.objects.get(id=id)
            serializer = ProductsSerializer(product)
            return Response(serializer.data)
        else:
            products = Products.objects.all()
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data)
    
    def get_permissions(self):
        # Override the get_permissions method to apply custom permissions only for the POST method
        if self.request.method == 'POST':
            return [IsAuthenticated, IsVendorUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        is_vendor = Vendor.objects.filter(user=user).exists()

        if is_vendor:
            serializer.save()
        else:
            raise PermissionDenied("Only vendors can create products.")
    
class OrdersView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)