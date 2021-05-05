from django.http import HttpResponse

from .models import Product
from .filters import ProductFilter
from .serializers import ProductListSerializer, ProductDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_class = ProductFilter
    
    def get_queryset(self):
        return Product.objects.all()
    
    
class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailsSerializer
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))

