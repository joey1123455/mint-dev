# profile/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serilizers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
