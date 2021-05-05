from rest_framework import serializers
from .models import UserProfile


class UserProfileNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    date_of_birth = serializers.DateField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'date_of_birth', 'phone_number', 'gender', 'bio']

