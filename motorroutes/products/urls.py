from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='ProductList'),
    path('<int:product_id>/', views.ProductDetails.as_view(), name='ProductDetails'),

]
