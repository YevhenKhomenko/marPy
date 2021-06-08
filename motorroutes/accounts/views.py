from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from .models import UserProfile, UserAuthCredentials
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer, EmailVerificationSerializer
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, GoogleSocialAuthSerializer
from .socials import Google
from .social_auth import authenticate_social_user
from .renderers import UserRenderer
from .tasks import send_verification_email

import jwt


class UserProfileList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


# TODO: write object permissions
class UserProfileDetails(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDetailsSerializer
    # permission_classes = [IsAuthenticated]

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
        current_site = get_current_site(request).domain
        send_verification_email.delay(user_id=user.id, current_site=current_site)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            user_auth_info = UserAuthCredentials.objects.get(user=user)
            if not user_auth_info.is_verified:
                user_auth_info.is_verified = True
                user_auth_info.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            if user is not None:
                send_verification_email.delay(user_id=user.id, current_site=get_current_site(request).domain)
            return Response({'error': 'Activation Expired. Another verification email was sent'},
                            status=status.HTTP_400_BAD_REQUEST)
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


class GoogleAuthRedirectEndpointView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def get(self, request):
        code = request.GET.get('code')
        try:
            validated_user_credentials = Google.validate(code)
            print(validated_user_credentials)
        except Exception:
            raise AuthenticationFailed('Authentication failed. Try again.')

        iss = validated_user_credentials.get('iss', None)  # must be 'https://accounts.google.com'
        aud = validated_user_credentials.get('aud', None)
        sub = validated_user_credentials.get('sub', None)  # unique google user id

        name = validated_user_credentials.get('name', 'default name')
        email = validated_user_credentials.get('email', None)
        provider = 'google'
        access = validated_user_credentials['access']
        refresh = validated_user_credentials['refresh']
        print('got data from user cred in view')
        if not (sub and aud) or iss != 'https://accounts.google.com':
            raise AuthenticationFailed('Authentication failed. Try again.')

        social_auth_resp = authenticate_social_user(
            provider=provider,
            user_id=sub,
            email=email,
            name=name,
            access_token=access,
            refresh_token=refresh)

        return Response(data=social_auth_resp, status=status.HTTP_200_OK)


class GoogleAuthGetUrlView(generics.GenericAPIView):
    def get(self, request):
        auth_url = Google.get_authorization_url()
        return HttpResponseRedirect(auth_url)




