from django.test import TestCase
from django.test import Client
# Create your tests here.
from coffee.models import Inventory_Item


# TODO:

class Inventory_ItemTestCase(TestCase):
    def setUp(self):
        Inventory_Item.objects.create(name='Milk', quantity=4, price=0.35)
        Inventory_Item.objects.create(name='Ice', quantity=20, price=0.20)


class URLTests(TestCase):
    def test_testLoginPage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    # https://docs.djangoproject.com/en/4.1/topics/testing/tools/#:~:text=Overview%20and%20a%20quick%20example%C2%B6
    def testSignin(self):
        c = Client()
        response = c.post('/login/', {'username': 'Test', 'password': 'Test12345'})
        self.assertEqual(response.status_code, 200)
