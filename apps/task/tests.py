from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.test import force_authenticate


class AuthentificationTestCase(APITestCase):
    def test_registration(self):
        data = {"first_name": "ION", "last_name": "Moraru", "username": "stepan", "password": "ricardo", }
        response = self.client.post(reverse('token_register'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogInTestCase(APITestCase):

    @classmethod
    def test_setUp(self):
        self.user = User.objects.create(username='Billy', password='Milligan')
        Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.get('token_obtain_pair')
        force_authenticate(self.request, user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
