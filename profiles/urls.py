# urls.py
from django.urls import path, include
from .views import VendorCreateAPIView, VendorListAPIView, VendorDetailAPIView, CustomerCreateAPIView, CustomerListAPIView, CustomerDetailAPIView, CreateCustomerSerializer

urlpatterns = [
    path('vendors/create/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('vendors/list', VendorListAPIView.as_view(), name='vendor-list'),
    path('vendors/<uuid:vendor_id>', VendorDetailAPIView.as_view(), name='vendor-detail-api'),
    path('customer/create/', CustomerCreateAPIView.as_view(), name='vendor-create'),
    path('customer/list', CustomerListAPIView.as_view(), name='vendor-list'),
    path('customer/<uuid:vendor_id>', CustomerDetailAPIView.as_view(), name='vendor-detail-api'),
]
