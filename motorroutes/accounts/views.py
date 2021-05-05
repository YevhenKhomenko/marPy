from .models import UserProfile
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))

