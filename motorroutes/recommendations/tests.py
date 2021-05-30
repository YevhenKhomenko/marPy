from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utils.helpers_for_tests import create_user, dump, login_user
from recommendations.models import Place, Similarity, OnlineLink

class RecommendationsAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        # self.manufacturer = Manufacturer.objects.create(name='test', description='test d')
        self.admin = create_user('admin@staff')

    def test_empty_get(self):
        response = self.c.get('/api/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_validation(self):
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

    def test_create(self):
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
            p = Place.objects.get(id=response.data['id'])
            self.assertEqual(response.data, {
                'id': 1,
                'title': "test1",
                'description': "test2"
            })
