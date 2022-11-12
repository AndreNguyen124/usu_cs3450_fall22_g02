from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from coffee.models import Inventory_Item


# Create your tests here.


class Inventory_ItemTestCase(TestCase):
    def setUp(self):
        Inventory_Item.objects.create(name='Milk', quantity=4, price=0.35)
        Inventory_Item.objects.create(name='Ice', quantity=20, price=0.20)


class URLTests(TestCase):
    def test_testLoginPage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_testRegisterPage(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_testUserViewPage(self):
        response = self.client.get('/userView/')
        self.assertEqual(response.status_code, 302)

    def test_testSignin(self):
        response = self.client.get('/login/')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(logged_in)

    # TODO: Need to determine how to test Redirect
    # def test_testSigninRedirect(self):
        # response = self.client.get('/login/')
        # user = User.objects.create(username='testuser')
        # user.set_password('12345')
        # user.save()
        # c = Client()
        # logged_in = c.login(username='testuser', password='12345')
        # self.assertRedirects(response, 'http://127.0.0.1:8000/userView/', 200)
