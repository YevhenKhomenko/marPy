import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet
from .models import UserPoint


class UserPointFilter(FilterSet):

    def search_filter(self, qs, name, value):
        return qs.filter(
            Q(point__icontains=value) | Q(userprofile__icontains=value)
        )

    search = django_filters.filters.CharFilter(method='search_filter')

    #
    class Meta:
        model = UserPoint
        fields = ['search', ]
