from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthentificationTestCase(APITestCase):
    def test_registration(self):
        data = {"first_name": "ION", "last_name": "Moraru", "username": "stepan", "password": "ricardo", }
        response = self.client.post(reverse('token_register'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogInTestCase(APITestCase):
    list_url = reverse("task_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="zxc", password="zxc")
        cls.token = Token.objects.create(user=cls.user)
        cls.test_api_authentification()

    def test_api_authentification(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_task_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_list_unauth(self):
        self.client.force_authentificate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
