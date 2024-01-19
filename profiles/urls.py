# urls.py
from django.urls import path, include
from .views import VendorCreateAPIView, VendorListAPIView, VendorDetailAPIView

urlpatterns = [
    path('vendors/create/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('vendors/list', VendorListAPIView.as_view(), name='vendor-list'),
    path('vendors/<uuid:vendor_id>', VendorDetailAPIView.as_view(), name='vendor-detail-api'),
]
