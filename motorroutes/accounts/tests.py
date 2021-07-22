from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from utils.helpers_for_tests import create_user, dump, login_user

from django.contrib.auth.models import User
from .models import UserProfile, UserAuthCredentials


class AccountsApiTest(APITestCase):

    @staticmethod
    def reg_test_user(username, email, first_name, last_name, password):
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        user_auth_cred = UserAuthCredentials.objects.create(
            user=user,
            is_verified=True
        )
        user_auth_cred.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()

    def login_test_user(self, email, password):
        login_url = reverse('login')
        login_data = {
            'email': email,
            'password': password
        }
        response = self.client.post(login_url, login_data, format='json')

        tokens = response.data.get('tokens', [])
        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        authorized_user = User.objects.get(email=response.data['email'])
        user_profile_pk = UserProfile.objects.get(user=authorized_user).pk
        user_id = authorized_user.id
        return {'user_profile_pk': user_profile_pk, 'user_id': user_id, 'refresh': tokens['refresh']}

    def setUp(self):

        self.test_user_email = 'test@test.com'
        self.test_user_password = 'Saf3Pas5W0rD'
        self.test_user_username = 'test_user'
        self.test_user_first_name = 'first name'
        self.test_user_last_name = 'last name'

        self.reg_test_user(
            username=self.test_user_username,
            email=self.test_user_email,
            first_name=self.test_user_first_name,
            last_name=self.test_user_last_name,
            password=self.test_user_password
            )

    def test_user_created(self):
        queryset = User.objects.filter(email='test@test.com')
        self.assertEqual(queryset.count(), 1)

    def test_user_reg_api(self):
        reg_url = reverse('register')
        reg_data = {
            'password': 'Saf3Pas5W0rD',
            'password2': 'Saf3Pas5W0rD',
            'email': 'test_api_reg@test.com',
            'username': 'user_reg_test_api',
            'first_name': 'test_first_reg',
            'last_name': 'test_last_reg'
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

    def test_user_reg_api_fail(self):
        reg_url = reverse('register')
        reg_data = {
            'password': self.test_user_password,
            'password2': self.test_user_password,
            'username': self.test_user_username,
            'email': self.test_user_email,
            'first_name': self.test_user_first_name,
            'last_name': self.test_user_last_name
        }
        response = self.client.post(reg_url, reg_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_api(self):
        login_url = reverse('login')
        login_data = {
            'email': self.test_user_email,
            'password': self.test_user_password
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
            'email': self.test_user_email,
            'password': '123WRONGPaSsWORD123'
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_details_api(self):
        user_login_info_dict = self.login_test_user(email=self.test_user_email, password=self.test_user_password)
        user_profile_pk = user_login_info_dict['user_profile_pk']
        profile_details_url = '/api/accounts/{}/'.format(user_profile_pk)
        response = self.client.get(profile_details_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_profile_details_api(self):
        user_login_info_dict = self.login_test_user(email=self.test_user_email, password=self.test_user_password)
        user_profile_pk = user_login_info_dict['user_profile_pk']
        user_id = user_login_info_dict['user_id']
        profile_details_url = '/api/accounts/{}/'.format(user_profile_pk)
        profile_data = {
            "phone_number": "380952788214",
            "user": {
                "id": user_id,
                "email": self.test_user_email,
                "username": self.test_user_username,
                "first_name": self.test_user_first_name,
                "last_name": self.test_user_last_name
            },
            "bio": "api test user bio",
            "gender": "m",
            "date_of_birth": "2021-06-07"
        }

        response = self.client.put(profile_details_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_profile_info_permission_fail(self):
        user_login_info_dict = self.login_test_user(email=self.test_user_email, password=self.test_user_password)
        user_profile_pk = user_login_info_dict['user_profile_pk']
        user_id = user_login_info_dict['user_id']

        profile_details_url = '/api/accounts/{}/'.format(user_profile_pk)
        profile_data = {
            "phone_number": "380952788214",
            "user": {
                "id": user_id,
                "email": self.test_user_email,
                "username": self.test_user_username,
                "first_name": self.test_user_first_name,
                "last_name": self.test_user_last_name
            },
            "bio": "api test user bio",
            "gender": "m",
            "date_of_birth": "2021-06-07"
        }

        self.reg_test_user(
            username='permission_fail',
            email='permission@fail.com',
            first_name='permission_fail_first',
            last_name='permission_fail_last',
            password=self.test_user_password
        )
        self.login_test_user(
                    email='permission@fail.com',
                    password=self.test_user_password
        )

        response = self.client.put(profile_details_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_api(self):
        user_login_info_dict = self.login_test_user(email=self.test_user_email, password=self.test_user_password)
        request_data = {
            'refresh': user_login_info_dict['refresh']
        }
        logout_url = reverse('logout')
        response = self.client.post(logout_url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_api_fail(self):
        user_login_info_dict = self.login_test_user(email=self.test_user_email, password=self.test_user_password)
        request_data = {
            'refresh': user_login_info_dict['refresh']
        }
        logout_url = reverse('logout')
        self.client.post(logout_url, request_data, format='json')
        response = self.client.post(logout_url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




