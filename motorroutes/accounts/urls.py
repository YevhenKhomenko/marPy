from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('', views.UserProfileList.as_view(), name='UserProfileList'),
    path('<int:user_profile_id>/', views.UserProfileDetails.as_view(), name='UserProfileDetails'),
    path('login/', views.ObtainTokenPairCustomView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),

]
