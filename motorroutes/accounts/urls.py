from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserProfileList.as_view(), name='UserProfileList'),
    path('<int:user_profile_id>/', views.ProductDetails.as_view(), name='UserProfileDetails'),
]
