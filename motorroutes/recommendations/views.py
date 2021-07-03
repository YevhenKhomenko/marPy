from .models import UserPoint, Similarity, UserRoute
from navigation.models import UserLocation, Points, Routes
from accounts.models import UserProfile
from .serializers import UserPointListSerializer, UserPointDetailsSerializer, SimilarityListSerializer, \
    SimilarityDetailsSerializer, UserRouteListSerializer, UserRouteDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination
from .filters import UserPointFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from statistic.models import Statistic
from rest_framework.response import Response
from rest_framework import status
import math
from navigation.serializers import PointsDetailsSerializer

class UserPointList(generics.ListCreateAPIView):
    queryset = UserPoint.objects.all()
    serializer_class = UserPointListSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_class = UserPointFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserPointDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPointDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, request):
        if request.method == 'GET':
            pass
        return get_object_or_404(UserPoint, pk=self.kwargs.get('userpoint_id'))


class SimilarityList(generics.ListCreateAPIView):
    queryset = Similarity.objects.all()
    serializer_class = SimilarityListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class SimilarityDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimilarityDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Similarity, pk=self.kwargs.get('similarity_id'))


class UserRouteList(generics.ListCreateAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserRouteDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRouteDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(UserRoute, pk=self.kwargs.get('userroute_id'))


class GetNearest():
    def get_nearest_point(self, point):
        # SQRT( POW(111.2 * (latitude - [startlat]), 2) +  POW(111.2 * ([startlng] - longitude) * COS(latitude / 57.3), 2)) AS distance
        all_attractions = Points.objects.get(attractions=True)
        d = {}
        for row in all_attractions:
            d['id'] = row['id']
            d['distance'] = math.sqrt(pow(111.2 * (row['latitude'] - point['latitude']), 2) + pow(
                111.2 * (point['latitude'] - row['latitude']) * math.cos(row['latitude'] / 57.3)))
        marklist = sorted((value, key) for (key, value) in d.items())[::-1][0:5]
        sort_d = dict([(k, v) for v, k in marklist])
        print(sort_d)
        return sort_d


class PointView(generics.GenericAPIView):

    def get(self, request):
        point_data = request.GET
        point = Points.objects.get_or_create(
            title=point_data['title'],
            latitude=point_data['latitude'],
            longitude=point_data['longitude'],
        )
        userprofile = UserProfile.objects.get(id=point_data['userprofile'])
        userpoint = UserPoint.objects.get_or_create(
            userprofile=userprofile,
            point=point[0],
        )
        queryset = Points.objects.filter(attractions=True)
        d = {}
        for row in queryset:
            distance = math.sqrt(pow(111.2 * (getattr(row, 'latitude') - getattr(point[0], 'latitude')), 2) + pow(
                111.2 * (getattr(point[0], 'longitude') - getattr(row, 'longitude')) * math.cos(
                    getattr(row, 'latitude')) / 57.3, 2))
            d[getattr(row, 'id')] = {'distance': distance }
        sorted_d = sorted(d.items(), key=lambda k_v: k_v[1]['distance'])
        list_id = {k:v for k, v in sorted_d[0:5]}
        print(list_id)
        return Response(list_id, status=status.HTTP_200_OK)
