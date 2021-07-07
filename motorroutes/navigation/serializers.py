from rest_framework import serializers
from .models import UserLocation, Points, Routes
from accounts.serializers import UserNestedSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class ValidationMixIn():

    def validate_userlocation(self, data):
        l_count = UserLocation.objects.filter(id=data.get('id')).count()
        if l_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong UserLocation id")

    def validate_points(self, data):
        p_count = Points.objects.filter(id=data.get('id')).count()
        if p_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong Place id")


class UserLocationNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    user = UserNestedSerializer(read_only=True)
    lat = serializers.FloatField(read_only=True)
    lon = serializers.FloatField(read_only=True)

    class Meta:
        model = UserLocation
        fields = ['id', 'user', 'lat', 'lon']


class UserLocationListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = UserLocation
        fields = ['id', 'user', 'lat', 'lon']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance = super().update(instance, validated_data)
        user = get_object_or_404(User, id=user_data.get('id'))
        instance.user = user
        instance.save()
        return instance


class UserLocationDetailsSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = UserLocation
        fields = ['id', 'user', 'lat', 'lon']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance = super().update(instance, validated_data)
        user = get_object_or_404(User, id=user_data.get('id'))
        instance.user = user
        instance.save()
        return instance


class PointsNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    userlocation = UserLocationNestedSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    ratingvoicecount = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    worktime = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    foundingdate = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    website = serializers.CharField(read_only=True)
    latlongdms = serializers.CharField(read_only=True)
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    class Meta:
        model = Points
        fields = ['id', 'title', 'description', 'rating', 'ratingvoicecount', 'phone', 'worktime',
                  'category', 'foundingdate', 'email', 'website', 'latlongdms', 'latitude', 'longitude', 'userlocation']



class PointsListSerializer(serializers.ModelSerializer):
    userlocation = UserLocationNestedSerializer()

    class Meta:
        model = Points
        fields = ['id', 'title', 'latlongdms', 'latitude', 'longitude', 'userlocation','attractions']

    def update(self, instance, validated_data):
        userlocation_data = validated_data.pop('userlocation')
        instance = super().update(instance, validated_data)
        userlocation = get_object_or_404(UserLocation, id=userlocation_data.get('id'))
        instance.userlocation = userlocation
        instance.save()
        return instance


class PointsDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    userlocation = UserLocationNestedSerializer()

    class Meta:
        model = Points
        fields = ['id', 'title', 'description', 'rating', 'ratingvoicecount', 'phone', 'worktime',
                  'category', 'foundingdate', 'email', 'website', 'latlongdms', 'latitude', 'longitude', 'userlocation']

    def update(self, instance, validated_data):
        userlocation_data = validated_data.pop('userlocation')
        instance = super().update(instance, validated_data)
        userlocation = get_object_or_404(UserLocation, id=userlocation_data.get('id'))
        instance.userlocation = userlocation
        instance.save()
        return instance


class RoutesNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    points = PointsNestedSerializer(read_only=True)
    distance = serializers.FloatField(read_only=True)
    shared_with = UserNestedSerializer(read_only=True)

    class Meta:
        model = Routes
        fields = ['id', 'points', 'distance', 'shared_with']


class RoutesListSerializer(serializers.ModelSerializer):
    points = PointsNestedSerializer()

    class Meta:
        model = Routes
        fields = ['id', 'points', 'distance']


    def update(self, instance, validated_data):
        points_data = validated_data.pop('points')
        instance = super().update(instance, validated_data)
        points = get_object_or_404(Points, id=points_data.get('id'))
        instance.points = points
        instance.save()
        return instance


class RoutesDetailsSerializer(serializers.ModelSerializer):
    points = PointsNestedSerializer()
    shared_with = UserNestedSerializer()

    class Meta:
        model = Routes
        fields = ['id', 'points', 'distance', 'shared_with']

    def update(self, instance, validated_data):
        points_data = validated_data.pop('points')
        instance = super().update(instance, validated_data)
        points = get_object_or_404(Points, id=points_data.get('id'))
        instance.points = points
        instance.save()
        return instance