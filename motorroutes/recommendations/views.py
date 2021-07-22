from .models import UserPoint, Similarity, UserRoute
from navigation.models import UserLocation, Points, Routes
from .serializers import UserPointListSerializer, UserPointDetailsSerializer, SimilarityListSerializer, \
    SimilarityDetailsSerializer, UserRouteListSerializer, UserRouteDetailsSerializer,PointViewSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination
from .filters import UserPointFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .calculate import GetNearest
from django.contrib.auth.models import User

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



class PointView(generics.GenericAPIView):

    def get(self, request):
        point_data = request.GET
        point = Points.objects.get_or_create(
            title=point_data['title'],
            latitude=point_data['latitude'],
            longitude=point_data['longitude'],
        )
        user = User.objects.get(id=point_data['user'])
        userpoint = UserPoint.objects.get_or_create(
            user=user,
            point=point[0],
        )
        result = GetNearest().get_nearest_points(point)
        return Response(result, status=status.HTTP_200_OK)
