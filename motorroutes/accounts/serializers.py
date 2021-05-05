from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


# TODO: UserRegisterSerializer


class UserNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email']


class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number']


class UserProfileDetailsSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'photo', 'user', 'created_by', 'bio', 'gender']
