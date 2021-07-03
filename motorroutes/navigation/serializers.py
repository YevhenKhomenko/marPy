from rest_framework import serializers
from .models import UserLocation, Points, Routes
from accounts.models import UserProfile
from accounts.serializers import UserProfileNestedSerializer
from django.shortcuts import get_object_or_404


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
    userprofile = UserProfileNestedSerializer()
    user_lat = serializers.FloatField(read_only=True)
    user_lon = serializers.FloatField(read_only=True)

    class Meta:
        model = UserLocation
        fields = ['id', 'userprofile', 'user_lat', 'user_lon']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserLocationListSerializer(serializers.ModelSerializer):
    userprofile = UserLocationNestedSerializer()

    class Meta:
        model = UserLocation
        fields = ['id', 'userprofile', 'user_lat', 'user_lon']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserLocationDetailsSerializer(serializers.ModelSerializer):
    userprofile = UserLocationNestedSerializer()

    class Meta:
        model = UserLocation
        fields = ['id', 'userprofile', 'user_lat', 'user_lon']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.save()
        return instance


class PointsNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    userlocation = UserLocationNestedSerializer()
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

    def update(self, instance, validated_data):
        userlocation_data = validated_data.pop('userlocation')
        instance = super().update(instance, validated_data)
        userlocation = get_object_or_404(UserLocation, id=userlocation_data.get('id'))
        instance.userprofile = userlocation
        instance.save()
        return instance


class PointsListSerializer(serializers.ModelSerializer):
    userlocation = UserLocationNestedSerializer()

    class Meta:
        model = Points
        fields = ['id', 'title', 'latlongdms', 'latitude', 'longitude', 'userlocation','attractions']

    def update(self, instance, validated_data):
        userlocation_data = validated_data.pop('userlocation')
        instance = super().update(instance, validated_data)
        userlocation = get_object_or_404(UserLocation, id=userlocation_data.get('id'))
        instance.userprofile = userlocation
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
        instance.userprofile = userlocation
        instance.save()
        return instance


class RoutesNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    points = PointsNestedSerializer()
    distance = serializers.FloatField(read_only=True)
    shared_with = UserProfileNestedSerializer()

    class Meta:
        model = Routes
        fields = ['id', 'points', 'distance', 'shared_with']

    def update(self, instance, validated_data):
        points_data = validated_data.pop('points')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        points = get_object_or_404(Points, id=points_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.points = points
        instance.save()
        return instance

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
    shared_with = UserProfileNestedSerializer()

    class Meta:
        model = Routes
        fields = ['id', 'points', 'distance', 'shared_with']

    def update(self, instance, validated_data):
        points_data = validated_data.pop('points')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        points = get_object_or_404(Points, id=points_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.userprofile = userprofile
        instance.points = points
        instance.save()
        return instance