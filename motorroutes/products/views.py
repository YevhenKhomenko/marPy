from django.http import HttpResponse

from .models import Product
from .serializers import ProductListSerializer, ProductDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    
    
class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailsSerializer
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))

