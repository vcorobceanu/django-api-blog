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

    def setUp(self):
        self.user = User.objects.create(username='Billy', password='Milligan')
        Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.get('token_obtain_pair')
        force_authenticate(self.request, user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_task(self):
        self.client.post(reverse('post_task'), {"title": "413",
                                                "description": "238",
                                                "status": "open",
                                                "is_started": "False",
                                                "author": "1",
                                                "assigned": "1"})

    def test_post_comm(self):
        self.client.post(reverse('post_comm'), {"text": "yardage",
                                                "author": "1",
                                                "task": "4"})

    def test_get_task(self):
        response = self.client.get(reverse('task_by_id', args=[4]))
        self.assertEqual(response.data, {"assigned": "1",
                                         "author": "1",
                                         "description": "8",
                                         "id": "4",
                                         "is_started": "False",
                                         "status": "closed",
                                         "title": "4"})
