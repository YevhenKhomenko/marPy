from django.urls import path

from . import views

urlpatterns = [
    path('userlocation/', views.UserLocationList.as_view(), name='UserLocationList'),
    path('userlocation/<int:userlocation_id>/', views.UserLocationDetails.as_view(), name='UserLocationDetails'),
    path('', views.PointsList.as_view(), name='PointsList'),
    path('<int:points_id>/', views.PointsDetails.as_view(), name='PointsDetails'),
    path('route/', views.RoutesList.as_view(), name='RoutesList'),
    path('route/<int:userroute_id>/', views.RoutesDetails.as_view(), name='RoutesDetails'),
]
