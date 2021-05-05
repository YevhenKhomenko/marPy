import django_filters
from django.conf import settings

from django.db.models import Q
from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):

    def search_filter(self, qs, name, value):
        return qs.filter(
            Q(name__icontains=value)|Q(description__icontains=value)
        )


    search = django_filters.filters.CharFilter(method='search_filter')
    #
    class Meta:
        model = Product
        fields = ['search',]

