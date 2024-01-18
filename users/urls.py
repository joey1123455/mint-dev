# myapp/urls.py
from django.urls import path
from .views import UserRegistrationView, LoginSerializer


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginSerializer.as_view(), name='login'),
]
