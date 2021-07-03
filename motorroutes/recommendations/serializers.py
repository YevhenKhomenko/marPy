from rest_framework import serializers
from .models import Similarity, UserPoint, UserRoute
from accounts.models import UserProfile
from accounts.serializers import UserProfileNestedSerializer
from django.shortcuts import get_object_or_404
from navigation.models import UserLocation, Points, Routes
from navigation.serializers import PointsNestedSerializer, RoutesNestedSerializer


class ValidationMixIn():
    def validate_userprofile(self, data):
        u_count = UserProfile.objects.filter(id=data.get('id')).count()
        if u_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong UserProfile id")


class UserPointNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    userprofile = UserProfileNestedSerializer()
    point = PointsNestedSerializer()

    class Meta:
        model = UserPoint
        fields = ['id', 'userprofile', 'point']

    def update(self, instance, validated_data):
        point_data = validated_data.pop('point')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        point = get_object_or_404(Points, id=point_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.point = point
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserPointListSerializer(serializers.ModelSerializer, ValidationMixIn):
    userprofile = UserProfileNestedSerializer()
    point = PointsNestedSerializer()

    class Meta:
        model = UserPoint
        fields = ['id', 'userprofile', 'point']

    def update(self, instance, validated_data):
        point_data = validated_data.pop('point')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        point = get_object_or_404(Points, id=point_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.point = point
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserPointDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    userprofile = UserProfileNestedSerializer()
    point = PointsNestedSerializer()

    class Meta:
        model = UserPoint
        fields = ['id', 'userprofile', 'point']

    def update(self, instance, validated_data):
        point_data = validated_data.pop('point')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        point = get_object_or_404(Points, id=point_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.point = point
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserRouteListSerializer(serializers.ModelSerializer, ValidationMixIn):
    userprofile = UserProfileNestedSerializer()
    route = RoutesNestedSerializer()

    class Meta:
        model = UserRoute
        fields = ['id', 'userprofile', 'route']

    def update(self, instance, validated_data):
        route_data = validated_data.pop('route')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        route = get_object_or_404(Routes, id=route_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.route = route
        instance.userprofile = userprofile
        instance.save()
        return instance


class UserRouteDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    userprofile = UserProfileNestedSerializer()
    route = RoutesNestedSerializer()

    class Meta:
        model = UserRoute
        fields = ['id', 'userprofile', 'route']

    def update(self, instance, validated_data):
        route_data = validated_data.pop('route')
        userprofile_data = validated_data.pop('userprofile')
        instance = super().update(instance, validated_data)
        route = get_object_or_404(Routes, id=route_data.get('id'))
        userprofile = get_object_or_404(UserProfile, id=userprofile_data.get('id'))
        instance.route = route
        instance.userprofile = userprofile
        instance.save()
        return instance


class SimilarityNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    attraction_point = PointsNestedSerializer()
    user_point = UserPointNestedSerializer()
    similarity_score = serializers.DecimalField(max_digits=20, decimal_places=20, read_only=True)

    class Meta:
        model = Similarity
        fields = ['id', 'attraction_point', 'user_point', 'similarity_score']

    def update(self, instance, validated_data):
        attraction_point_data = validated_data.pop('attraction_point')
        user_point_data = validated_data.pop('user_point')
        instance = super().update(instance, validated_data)
        attraction_point = get_object_or_404(Points, id=attraction_point_data.get('id'))
        user_point = get_object_or_404(UserPoint, id=user_point_data.get('id'))
        instance.attraction_point = attraction_point
        instance.user_point = user_point
        instance.save()
        return instance


class SimilarityListSerializer(serializers.ModelSerializer):
    attraction_point = PointsNestedSerializer()
    user_point = UserPointNestedSerializer()

    class Meta:
        model = Similarity
        fields = ['id', 'attraction_point', 'user_point', 'similarity_score']

    def update(self, instance, validated_data):
        attraction_point_data = validated_data.pop('attraction_point')
        user_point_data = validated_data.pop('user_point')
        instance = super().update(instance, validated_data)
        attraction_point = get_object_or_404(Points, id=attraction_point_data.get('id'))
        user_point = get_object_or_404(UserPoint, id=user_point_data.get('id'))
        instance.attraction_point = attraction_point
        instance.user_point = user_point
        instance.save()
        return instance


class SimilarityDetailsSerializer(serializers.ModelSerializer, ValidationMixIn):
    attraction_point = PointsNestedSerializer()
    user_point = UserPointNestedSerializer()

    class Meta:
        model = Similarity
        fields = ['id', 'attraction_point', 'user_point', 'similarity_score']

    def update(self, instance, validated_data):
        attraction_point_data = validated_data.pop('attraction_point')
        user_point_data = validated_data.pop('user_point')
        instance = super().update(instance, validated_data)
        attraction_point = get_object_or_404(Points, id=attraction_point_data.get('id'))
        user_point = get_object_or_404(UserPoint, id=user_point_data.get('id'))
        instance.attraction_point = attraction_point
        instance.user_point = user_point
        instance.save()
        return instance

