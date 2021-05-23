
from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utils.helpers_for_tests import create_user, dump, login_user
from products.models import Manufacturer, Product


class ProductsAPITest(TestCase):
    
    def setUp(self):
        self.c = APIClient()
        self.manufacturer = Manufacturer.objects.create(name='test', description='test d')
        self.admin = create_user('admin@staff')
    
    
    def test_empty_get(self):
        #print(dir(self))
        response = self.c.get('/api/product/')
        #print(response)
        #dump(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        
    def test_create_validation(self):
        #print(dir(self))
        response = self.c.post('/api/product/',
            data={
                'name': '123'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'description': [
                'This field is required.'
            ],
            'manufacturer': [
                'This field is required.'
            ]
        })
        
    def test_create(self):
        #print(dir(self))
        login_user(self.c, self.admin)
        response = self.c.post('/api/product/',
            data={
                'name': '123',
                'description': '123',
                'vendor_code': 123,
                'manufacturer': {'id': self.manufacturer.id}
            },
            format='json'
        )
        dump(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        p = Product.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': 1,
            'name': "123",
            'description': "123",
            'manufacturer': {
                'id': 1,
                'name': "test",
                'description': "test d"
            },
            'created_on': response.data['created_on']
        })


