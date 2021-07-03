from .models import UserLocation, Points, Routes
from .serializers import UserLocationListSerializer, UserLocationDetailsSerializer, PointsListSerializer, \
    PointsDetailsSerializer, RoutesListSerializer, RoutesDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .filters import PointsFilter
from .permissions import IsOwnerOrReadOnly

class UserLocationList(generics.ListCreateAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserLocationDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserLocationDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, request):
        if request.method == 'GET':
            pass
        return get_object_or_404(UserLocation, pk=self.kwargs.get('userlocation_id'))


class PointsList(generics.ListCreateAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsListSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_class = PointsFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PointsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PointsDetailsSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Points, pk=self.kwargs.get('points_id'))


class RoutesList(generics.ListCreateAPIView):
    queryset = Routes.objects.all()
    serializer_class = RoutesListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class RoutesDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutesDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Routes, pk=self.kwargs.get('reutes_id'))
