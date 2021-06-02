from .models import Place, Similarity, OnlineLink
from .serializers import PlaceListSerializer, PlaceDetailsSerializer, SimilarityListSerializer, \
    SimilarityDetailsSerializer, OnlineLinkDetailsSerializer, OnlineLinkListSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination
from .filters import PlaceFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_class = PlaceFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class PlaceDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceDetailsSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Place, pk=self.kwargs.get('place_id'))


class SimilarityList(generics.ListCreateAPIView):
    queryset = Similarity.objects.all()
    serializer_class = SimilarityListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class SimilarityDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimilarityDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Place, pk=self.kwargs.get('similarity_id'))


class OnlineLinkList(generics.ListCreateAPIView):
    queryset = OnlineLink.objects.all()
    serializer_class = OnlineLinkListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class OnlineLinkDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OnlineLinkDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(OnlineLink, pk=self.kwargs.get('onlinelink_id'))
