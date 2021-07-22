from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import UserProfile, UserAuthCredentials


class ValidationMixIn:
    def validate_user_profile(self, data):
        u_count = UserProfile.objects.filter(id=data.get('id')).count()
        if u_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong UserProfile id")


class UserProfileNestedSerializer(serializers.ModelSerializer, ValidationMixIn):
    id = serializers.IntegerField()
    date_of_birth = serializers.DateField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'date_of_birth', 'phone_number', 'gender', 'bio']


class UserNestedSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'email', 'username']


class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number']


class UserProfileDetailsSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    # Was commented for testing purposes:
    # photo = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'user', 'bio', 'gender', 'date_of_birth']  # 'photo'

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.photo = validated_data.get('photo', instance.photo)
        user = instance.user
        instance.save()

        user_validated_data = validated_data['user']
        user.first_name = user_validated_data.get('first_name', user.first_name)
        user.last_name = user_validated_data.get('last_name', user.last_name)
        user.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'required': True},
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

        user_auth_info = UserAuthCredentials.objects.create(
            user=user,
            is_verified=False,
        )
        user_auth_info.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()

        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        user_auth_info = UserAuthCredentials.objects.get(user=user)
        return {
            'refresh': user_auth_info.get_tokens_for_user()['refresh'],
            'access': user_auth_info.get_tokens_for_user()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.get(email=email)
        username = filtered_user_by_email.username
        user = authenticate(username=username, password=password)
        user_auth_info = UserAuthCredentials.objects.get(user=filtered_user_by_email)

        if filtered_user_by_email and user_auth_info.auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + user_auth_info.auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user_auth_info.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return{
            'email': user.email,
            'username': user.username,
            'tokens': user_auth_info.get_tokens_for_user()
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')



