from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer
from .serializers import TokenObtainPairCustomSerializer
from .serializers import RegisterSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAdminUser]


class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))


class ObtainTokenPairCustomView(TokenObtainPairView):
    permission_classes = []
    serializer_class = TokenObtainPairCustomSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



