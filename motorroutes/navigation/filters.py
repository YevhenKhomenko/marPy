import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet
from .models import Points


class PointsFilter(FilterSet):

    def search_filter(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(latitude__icontains=value) | Q(longitude__icontains=value) | Q(attractions__icontains=value)
        )

    search = django_filters.filters.CharFilter(method='search_filter')

    #
    class Meta:
        model = Points
        fields = ['search', ]
