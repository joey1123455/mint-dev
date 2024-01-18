# Create your views here.
# myapp/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serialisers import UserSerializer
from django.contrib.auth import authenticate
from .serialisers import LoginSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response

class UserLoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response({'error': 'Invalid username or password'}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})