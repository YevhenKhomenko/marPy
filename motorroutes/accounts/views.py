from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer
from .serializers import TokenObtainPairCustomSerializer
from .serializers import RegisterSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))


class ObtainTokenPairCustomView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairCustomSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

