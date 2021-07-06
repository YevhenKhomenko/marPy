from django.urls import path, include
from motorroutes import settings

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('', views.UserProfileList.as_view(), name='user_profile_list'),
    path('<int:user_profile_id>/', views.UserProfileDetails.as_view(), name='user-profile-details'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verification/', views.VerifyEmailView.as_view(), name="email-verification"),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('oauth/google/', views.GoogleAuthRedirectEndpointView.as_view(), name='google_oauth'),
    path('login/google/', views.GoogleAuthGetUrlView.as_view(), name='get_google_auth_redirect_url'),
]
