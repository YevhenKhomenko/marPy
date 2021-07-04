from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from .models import UserProfile, UserAuthCredentials
from .permissions import IsProfileOwnerOrReadOnly
from .serializers import UserProfileListSerializer, UserProfileDetailsSerializer, EmailVerificationSerializer
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from .socials import Google
from .social_auth import authenticate_google_social_user
from .renderers import UserRenderer
from .tasks import send_verification_email

import jwt


class UserProfileList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


class UserProfileDetails(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
    serializer_class = UserProfileDetailsSerializer

    def get_object(self):
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))
        self.check_object_permissions(self.request, obj)
        return obj


class RegisterView(generics.GenericAPIView):
    """Creates user, user profile and user auth credentials, sends verification letter to user's email"""

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
        if settings.DEFERRED_OPERATIONS:
            send_verification_email.delay(user_id=user.id, current_site=current_site)
        else:
            send_verification_email(user_id=user.id, current_site=current_site)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    """Email verification url link endpoint. Verifies user token and completes registration"""

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
            return JsonResponse({'email': 'Successfully activated'},
                                status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            if user is not None:
                if settings.DEFERRED_OPERATIONS:
                    send_verification_email.delay(user_id=user.id, current_site=get_current_site(request).domain)
                else:
                    send_verification_email(user_id=user.id, current_site=get_current_site(request).domain)
            return JsonResponse({'error': 'Activation Expired. Another verification email was sent'},
                                status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return JsonResponse({'error': 'Invalid token. DecodeError'},
                                status=status.HTTP_400_BAD_REQUEST)


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
    """Callback view for google OAuth2"""

    def get(self, request):
        code = request.GET.get('code')
        try:
            validated_user_credentials = Google.fetch_google_user_info(code)
        except Exception:
            raise AuthenticationFailed('Authentication failed. Try again.')

        name = validated_user_credentials.get('name', 'default name')
        email = validated_user_credentials['email']
        sub = validated_user_credentials['sub']
        provider = 'google'
        access = validated_user_credentials['access']
        refresh = validated_user_credentials['refresh']

        social_auth_resp = authenticate_google_social_user(
            provider=provider,
            user_id=sub,
            email=email,
            name=name,
            access_token=access,
            refresh_token=refresh)

        return Response(data=social_auth_resp, status=status.HTTP_200_OK)


class GoogleAuthGetUrlView(generics.GenericAPIView):
    """Redirects to Google OAuth2"""
    def get(self, request):
        auth_url = Google.get_authorization_url()
        return HttpResponseRedirect(auth_url)




