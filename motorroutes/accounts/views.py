from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, UserAuthCredentials
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer, EmailVerificationSerializer
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, GoogleSocialAuthSerializer
from .renderers import UserRenderer
from .acc_utils import MailSenderUtil

import jwt


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAdminUser]


class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer, ]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verification')
        abs_url = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + abs_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        MailSenderUtil.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            print('before decoding')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print('after decoding')
            user = User.objects.get(id=payload['user_id'])
            user_auth_info = UserAuthCredentials.objects.get(user=user)
            if not user_auth_info.is_verified:
                user_auth_info.is_verified = True
                user_auth_info.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid token. DecodeError'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Successful logout", status=status.HTTP_204_NO_CONTENT)


class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['tokens']
        return Response(data, status=status.HTTP_200_OK)


