import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
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


class LogInTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Billy', password='Milligan')
        Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.get('token_obtain_pair')
        force_authenticate(self.request, user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_task(self):
        response = self.client.post(reverse('post_task'), {"title": "413",
                                                           "description": "238",
                                                           "status": "open",
                                                           "is_started": False,
                                                           "author": self.user.id,
                                                           "assigned": self.user.id})

        task = response.json()

        response1 = self.client.post(reverse('post_comm'), {"text": "yardage",
                                                            "author": self.user.id,
                                                            "task": task['id']})

        comment = response1.json()

        rez = self.client.get(reverse('task_by_id', args=[1]))
        self.assertEqual(json.dumps(rez.data), json.dumps(['Task : ',
                                                           {'id': task['id'],
                                                            'title': task['title'],
                                                            'description': task['description'],
                                                            'status': task['status'],
                                                            'is_started': task['is_started'],
                                                            'author': task['author'],
                                                            'assigned': task['assigned']},
                                                           'Comments : ',
                                                           [OrderedDict(
                                                               [('id', comment['id']),
                                                                ('text', comment['text']),
                                                                ('author', comment['author']),
                                                                ('task', comment['task'])])]]))
