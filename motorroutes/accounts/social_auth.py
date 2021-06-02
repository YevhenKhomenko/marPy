from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from .models import UserAuthCredentials


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 10000))
        return generate_username(random_username)


def authenticate_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        user = User.objects.get(email=email)
        user_auth_info = UserAuthCredentials.objects.get(user=user)
        if provider == user_auth_info.auth_provider:

            registered_user = authenticate(
                username=user.username, password=settings.SOCIAL_SECRET
            )
            registered_user_auth_info = UserAuthCredentials.objects.get(user=registered_user)

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user_auth_info.get_tokens_for_user()
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue login using ' + user_auth_info.auth_provider)

    else:
        username = generate_username(name)
        user = {
            'username': username, 'email': email,
            'password': settings.SOCIAL_SECRET
        }
        user = User.objects.create_user(**user)
        user.save()
        user_auth_info = UserAuthCredentials.objects.create(
            user=user, is_verified=True,
            auth_provider=provider
        )
        user_auth_info.save()

        new_user = authenticate(
            username=username, password=settings.SOCIAL_SECRET)
        new_user_auth_info = UserAuthCredentials.objects.get(user=new_user)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user_auth_info.get_tokens_for_user()
        }
