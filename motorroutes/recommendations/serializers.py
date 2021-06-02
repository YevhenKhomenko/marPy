from rest_framework import serializers
from .models import Place, Similarity, OnlineLink
from accounts.models import UserProfile
from accounts.serializers import UserProfileNestedSerializer
from django.shortcuts import get_object_or_404
from navigation.models import Location


class ValidationMixIn():
    def validate_userprofile(self, data):
        u_count = UserProfile.objects.filter(id=data.get('id')).count()
        if u_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong UserProfile id")

    # TODO: add validation to navigation serializers.py
    # def validate_location(self, data):
    #     l_count = Location.objects.filter(id=data.get('id')).count()
    #     if l_count == 1:
    #         return data
    #     else:
    #         raise serializers.ValidationError("wrong Location id")

    def validate_place(self, data):
        p_count = Location.objects.filter(id=data.get('id')).count()
        if p_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong Place id")


class PlaceNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'title', 'description']


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'title', 'description']


class PlaceDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    userprofile = UserProfileNestedSerializer()

    class Meta:
        model = Place
        fields = ['id', 'userprofile', 'title', 'description', 'user_ratings', 'num_rated', 'comparable',
                  'liked', 'location']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.save()
        return instance


class SimilarityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Similarity
        fields = ['id', 'first_place', 'second_place', 'similarity_score']


class SimilarityDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    first_place = PlaceNestedSerializer()
    second_place = PlaceNestedSerializer()

    class Meta:
        model = Similarity
        fields = ['id', 'first_place', 'second_place', 'similarity_score']

    def update(self, instance, validated_data):
        first_place_data = validated_data.pop('first_place')
        second_place_data = validated_data.pop('second_place')
        instance = super().update(instance, validated_data)
        first_place = get_object_or_404(Place, id=first_place_data.get('id'))
        second_place = get_object_or_404(Place, id=second_place_data.get('id'))
        instance.first_place = first_place
        instance.second_place = second_place
        instance.save()
        return instance


class OnlineLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineLink
        fields = ['id', 'place', 'userprofile']


class OnlineLinkDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    place = PlaceNestedSerializer()
    userprofile = UserProfileNestedSerializer()

    class Meta:
        model = OnlineLink
        fields = ['id', 'place', 'userprofile', 'gallery_id', 'blog_id', 'google_id']

    def update(self, instance, validated_data):
        place_data = validated_data.pop('place')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        place = get_object_or_404(UserProfile, id=place_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.place = place
        instance.userprofile = userprofile
        instance.save()
        return instance
