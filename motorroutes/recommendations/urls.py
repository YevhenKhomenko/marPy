from django.urls import path

from . import views

urlpatterns = [
    path('', views.PlaceList.as_view(), name='PlaceList'),
    path('<int:place_id>/', views.PlaceDetails.as_view(), name='PlaceDetails'),
    path('', views.SimilarityList.as_view(), name='SimilarityList'),
    path('<int:similarity_id>/', views.SimilarityDetails.as_view(), name='SimilarityDetails'),
    path('', views.OnlineLinkList.as_view(), name='OnlineLinkList'),
    path('<int:onlinelink_id>/', views.OnlineLinkDetails.as_view(), name='OnlineLinkDetails'),

]
