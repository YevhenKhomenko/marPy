from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utils.helpers_for_tests import create_user, dump, login_user
from recommendations.models import Place, Similarity, OnlineLink
from accounts.models import UserProfile
import datetime


class RecommendationsAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.admin = create_user('admin@staff')
        self.user = create_user('user@staff')
        self.userprofile = UserProfile.objects.create(phone_number='2144443432',
                                                      user=self.admin,
                                                      bio="34234",
                                                      gender="m",
                                                      date_of_birth=datetime.date(1997, 10, 19))

    def test_place_empty_get(self):
        login_user(self.c, self.admin)
        self.c.login()
        response = self.c.get('/api/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_place_create_validation(self):
        login_user(self.c, self.admin)
        self.c.login()
        response = self.c.post('/api/recommendations/',
                               data={
                                   "title": "",
                                   "description": ""
                               }
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "title": [
                "This field may not be blank."
            ],
            "description": [
                "This field may not be blank."
            ]
        })

    def test_place_create(self):
        # with self.settings(REST_FRAMEWORK={
        #     'DEFAULT_FILTER_BACKENDS': (
        #             'django_filters.rest_framework.DjangoFilterBackend',
        #     ), }):
        login_user(self.c, self.admin)
        self.c.login()
        response = self.c.post('/api/recommendations/',
                               data={
                                   "title": "test1",
                                   "description": "test2"
                               },
                               format='json'
                               )

        # dump(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data["id"],
            'title': "test1",
            'description': "test2"
        })

    def test_place_create_nested(self):
        login_user(self.c, self.admin)
        self.c.login()
        response = self.c.post('/api/recommendations/',
                               data={
                                   "id": 1,
                                   "userprofile": {"id": self.userprofile.id},
                                   "title": "1234",
                                   "description": "qwer",
                                   "user_ratings": 1.0,
                                   "num_rated": 2,
                                   "comparable": True,
                                   "liked": True,
                                   "location": None
                               },
                               format='json'
                               )

        # dump(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data["id"],
            'title': "1234",
            'description': "qwer"
        })

    def test_place_detail_update_nested(self):
        login_user(self.c, self.admin)
        response_create = self.c.post('/api/recommendations/',
                                      data={
                                          "userprofile": {"id": self.userprofile.id},
                                          "title": "1234",
                                          "description": "qwer",
                                          "user_ratings": 1.0,
                                          "num_rated": 2,
                                          "comparable": True,
                                          "liked": True,
                                          "location": None
                                      },
                                      format='json'
                                      )
        # dump(response_create)
        response_update = self.c.put(f'/api/recommendations/{response_create.data["id"]}/',
                                     {
                                         "id": response_create.data["id"],
                                         "userprofile": {"id": self.userprofile.id},
                                         "title": "1234",
                                         "description": "qwer",
                                         "user_ratings": 1.0,
                                         "num_rated": 2,
                                         "comparable": True,
                                         "liked": True,
                                         "location": None
                                     },
                                     format='json'
                                     )
        # dump(response_update)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data, {
            'id': response_update.data["id"],
            'userprofile': {
                'id': self.userprofile.id,
                'date_of_birth': "1997-10-19",
                'phone_number': "2144443432",
                'gender': "m",
                'bio': "34234"
            },
            'title': "1234",
            'description': "qwer",
            'user_ratings': 1.0,
            'num_rated': 2,
            'comparable': True,
            'liked': True,
            'location': None
        })

    def test_place_update_isOwner_permission(self):
        login_user(self.c, self.admin)
        self.c.login()
        response_admin_create = self.c.post('/api/recommendations/',
                               data={
                                   "title": "test1",
                                   "description": "test2"
                               },
                               format='json'
                               )
        login_user(self.c, self.user)
        self.c.login()
        response_user_update = self.c.put('/api/recommendations/',
                                          data={
                                              "id": response_admin_create.data["id"],
                                              "title": "test1",
                                              "description": "test2"
                                          },
                                          format='json'
                                          )
        # dump(response_user_update)
        self.assertEqual(response_user_update.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_user_update.data, {
            'detail': "Method \"PUT\" not allowed."
        })
