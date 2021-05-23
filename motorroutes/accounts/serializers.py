from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


# TODO: UserRegisterSerializer


class ValidationMixIn():
    def validate_user_profile(self, data):
        u_count = UserProfile.objects.filter(id=data.get('id')).count()
        if u_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong UserProfile id")


class UserNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email']


class UserProfileNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    date_of_birth = serializers.DateField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'date_of_birth', 'phone_number', 'gender', 'bio']


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


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairCustomSerializer, cls).get_token(user)

        # Adding custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


