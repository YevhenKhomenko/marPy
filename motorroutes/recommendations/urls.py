from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserPointList.as_view(), name='UserPointList'),
    path('<int:userpoint_id>/', views.UserPointDetails.as_view(), name='UserPointDetails'),
    path('s/', views.SimilarityList.as_view(), name='SimilarityList'),
    path('s/<int:similarity_id>/', views.SimilarityDetails.as_view(), name='SimilarityDetails'),
    path('r/', views.UserRouteList.as_view(), name='UserRouteList'),
    path('r/<int:userroute_id>/', views.UserRouteDetails.as_view(), name='UserRouteDetails'),
    path('point/', views.PointView.as_view(), name='PointList')
]
