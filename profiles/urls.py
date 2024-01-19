# profile/urls.py
from django.urls import path
from .views import CustomerCreateView

urlpatterns = [
    path('register_customer', CustomerCreateView.as_view(), name='customer-profile'),
]
