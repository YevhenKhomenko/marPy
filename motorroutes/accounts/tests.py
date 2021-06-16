from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from utils.helpers_for_tests import create_user, dump, login_user

from django.contrib.auth.models import User
from .models import UserProfile, UserAuthCredentials


class AccountsApiTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            first_name='first name',
            last_name='last name'
        )
        user.set_password('Saf3Pas5W0rD')
        user.save()

        user_auth_cred = UserAuthCredentials.objects.create(
            user=user,
            is_verified=True
        )
        user_auth_cred.save()

        self.access_token = None
        self.refresh_token = None
        self.user_profile_pk = None
        self.user_id = None
        self.email = 'test_api@test.com'
        self.username = 'user_test_api'
        self.first_name = 'test_first'
        self.last_name = 'test_last'

    def test_user_created(self):
        queryset = User.objects.filter(email='test@test.com')
        self.assertEqual(queryset.count(), 1)

    def test_user_reg_api(self):
        reg_url = reverse('register')
        reg_data = {
            'password': 'Saf3Pas5W0rD',
            'password2': 'Saf3Pas5W0rD',
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        response = self.client.post(reg_url, reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        queryset = User.objects.filter(email=response.data['email'])
        self.assertEqual(queryset.count(), 1)

        registered_user = User.objects.get(email=response.data['email'])
        registered_user_profile = UserProfile.objects.filter(user=registered_user)
        registered_user_credentials = UserAuthCredentials.objects.filter(user=registered_user)
        self.assertEqual(registered_user_profile.count(), 1)
        self.assertEqual(registered_user_credentials.count(), 1)

        registered_user_credentials = UserAuthCredentials.objects.get(user=registered_user)
        registered_user_credentials.set_verification_status(is_verified=True)

    def test_user_reg_api_fail(self):
        reg_url = reverse('register')
        reg_data = {
            'password': 'Saf3Pas5W0rD',
            'password2': 'Saf3Pas5W0rD',
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        response = self.client.post(reg_url, reg_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_api(self):
        login_url = reverse('login')
        login_data = {
            'email': self.email,
            'password': 'Saf3Pas5W0rD'
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tokens = response.data.get('tokens', [])
        self.assertEqual(len(tokens), 2)

        self.access_token = tokens['access']
        self.refresh_token = tokens['refresh']

    def test_user_login_api_fail(self):
        login_url = reverse('login')
        login_data = {
            'email': self.email,
            'password': '123WRONGPaSSWORD123'
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        authorized_user = User.objects.get(email=response.data['email'])
        self.user_profile_pk = UserProfile.objects.get(user=authorized_user).pk
        self.user_id = authorized_user.id

    def test_get_profile_details_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))
        profile_details_url = '/api/accounts/{}/'.format(self.user_profile_pk)
        response = self.client.get(profile_details_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_profile_details_api(self):
        profile_details_url = '/api/accounts/{}/'.format(self.user_profile_pk)
        profile_data = {
            "phone_number": "380952788214",
            "user": {
                "id": self.user_id,
                "email": self.email,
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name
            },
            "bio": "api test user bio",
            "gender": "m",
            "date_of_birth": "2021-06-07"
        }

        response = self.client.put(profile_details_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_profile_info_permission_fail(self):
        login_data = {
            'email': 'test@test.com',
            'password': 'Saf3Pas5W0rD'
        }

        login_url = reverse('login')
        response = self.client.post(login_url, login_data, format='json')

        tokens = response.data.get('tokens', [])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access']))

        profile_details_url = '/api/accounts/{}/'.format(self.user_profile_pk)
        profile_data = {
            "phone_number": "380952788214",
            "user": {
                "id": self.user_id,
                "email": self.email,
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name
            },
            "bio": "api test user bio",
            "gender": "m",
            "date_of_birth": "2021-06-07"
        }
        response = self.client.put(profile_details_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))
        request_data = {
            'refresh': self.refresh_token
        }
        logout_url = reverse('logout')
        response = self.client.post(logout_url, request_data, format='json')




