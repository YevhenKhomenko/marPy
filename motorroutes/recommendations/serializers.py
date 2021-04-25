from rest_framework import serializers
from .models import Place, Similarity, OnlineLink
from accounts.models import User


class UserNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    date_of_birth = serializers.DateField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'date_of_birth', 'phone_number', 'gender', 'bio']


class PlaceNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'title', 'description']


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'title', 'description']


class PlaceDetailsSerializer(serializers.ModelSerializer):
    user_id = UserNestedSerializer()

    class Meta:
        model = Place
        fields = ['id', 'user_id', 'title', 'description', 'user_ratings', 'num_rated', 'comparable',
                  'liked']

    def update(self, instance, validated_data):
        user_id_data = validated_data.pop('user_id')
        instance = super().update(instance, validated_data)
        user_id = User.objects.get(pk=user_id_data.get('user_id'))
        instance.user_id = user_id
        instance.save()
        return instance


class SimilarityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Similarity
        fields = ['id', 'first_place', 'second_place', 'similarity_score']


class SimilarityDetailsSerializer(serializers.ModelSerializer):
    first_place = PlaceNestedSerializer()
    second_place = PlaceNestedSerializer()

    class Meta:
        model = Similarity
        fields = ['id', 'first_place', 'second_place', 'similarity_score']

    def update(self, instance, validated_data):
        first_place_data = validated_data.pop('first_place')
        second_place_data = validated_data.pop('second_place')
        instance = super().update(instance, validated_data)
        first_place = User.objects.get(pk=first_place_data.get('id'))
        second_place = User.objects.get(pk=second_place_data.get('id'))
        instance.first_place = first_place
        instance.second_place = second_place
        instance.save()
        return instance


class OnlineLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineLink
        fields = ['id', 'place', 'user_id']


class OnlineLinkDetailsSerializer(serializers.ModelSerializer):
    place = PlaceNestedSerializer()
    user_id = UserNestedSerializer()

    class Meta:
        model = OnlineLink
        fields = ['id', 'place', 'user_id', 'gallery_id', 'blog_id', 'google_id']

    def update(self, instance, validated_data):
        place_data = validated_data.pop('place')
        user_id_data = validated_data.pop('user_id')
        instance = super().update(instance, validated_data)
        place = User.objects.get(pk=place_data.get('id'))
        user_id = User.objects.get(pk=user_id_data.get('id'))
        instance.place = place
        instance.user_id = user_id
        instance.save()
        return instance
