from django.http import HttpResponse

from .models import Place, Similarity, OnlineLink
from .serializers import PlaceListSerializer, PlaceDetailsSerializer, SimilarityListSerializer, \
    SimilarityDetailsSerializer, OnlineLinkDetailsSerializer, OnlineLinkListSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializer


class PlaceDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceDetailsSerializer

    def get_object(self):
        return get_object_or_404(Place, pk=self.kwargs.get('place_id'))


class SimilarityList(generics.ListCreateAPIView):
    queryset = Similarity.objects.all()
    serializer_class = SimilarityListSerializer


class SimilarityDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimilarityDetailsSerializer

    def get_object(self):
        return get_object_or_404(Place, pk=self.kwargs.get('similarity_id'))


class OnlineLinkList(generics.ListCreateAPIView):
    queryset = OnlineLink.objects.all()
    serializer_class = OnlineLinkListSerializer


class OnlineLinkDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OnlineLinkDetailsSerializer

    def get_object(self):
        return get_object_or_404(OnlineLink, pk=self.kwargs.get('onlinelink_id'))
