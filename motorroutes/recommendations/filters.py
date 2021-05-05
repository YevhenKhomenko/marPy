import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet
from .models import Place,Similarity,OnlineLink


class PlaceFilter(FilterSet):

    def search_filter(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value)|Q(description__icontains=value)
        )


    search = django_filters.filters.CharFilter(method='search_filter')
    #
    class Meta:
        model = Place
        fields = ['search',]

