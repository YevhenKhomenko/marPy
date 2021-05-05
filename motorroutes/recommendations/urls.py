from django.urls import path

from . import views

urlpatterns = [
    path('', views.PlaceList.as_view(), name='PlaceList'),
    path('<int:place_id>/', views.PlaceDetails.as_view(), name='PlaceDetails'),
    path('/s', views.SimilarityList.as_view(), name='SimilarityList'),
    path('/s/<int:similarity_id>/', views.SimilarityDetails.as_view(), name='SimilarityDetails'),
    path('/o', views.OnlineLinkList.as_view(), name='OnlineLinkList'),
    path('/o/<int:onlinelink_id>/', views.OnlineLinkDetails.as_view(), name='OnlineLinkDetails'),

]
