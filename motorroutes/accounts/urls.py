from django.urls import path, include
from motorroutes import settings

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

oauth_api_urls = [
    path('', include('rest_framework_social_oauth2.urls')),
]


if settings.DEBUG:
    oauth_api_urls.append(path('verify/',  include('rest_framework.urls')))


urlpatterns = [
    path('', views.UserProfileList.as_view(), name='user_profile_list'),
    path('<int:user_profile_id>/', views.UserProfileDetails.as_view(), name='user_profile_details'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('email-verification/', views.VerifyEmailView.as_view(), name="email_verification"),
    path('login/', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='auth_logout'),
    path('oauth/google/', views.GoogleAuthRedirectEndpointView.as_view(), name='google_oauth'),
    path('login/google/', views.GoogleAuthGetUrlView.as_view(), name='google_auth_redirect_url'),
    #path('oauth/', include(oauth_api_urls))
]
