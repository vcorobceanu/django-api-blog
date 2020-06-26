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

        response1 = self.client.post(reverse('post_comm'), {"text": "yardage",
                                                            "author": self.user.id,
                                                            "task": response.json()['id']})

        b = {**response.json(), **response1.json()}
        rez = self.client.get(reverse('task_by_id', args=[1]))
        #self.assertEqual(rez.data, {**response.json(), **response1.json()})
        v = str(rez.data)
        s = "['Task : ', {'id': "+str(+response.json()['id'])+", 'title': '"+str(response.json()['title'])+"', 'description': '"+str(response.json()['description'])+"', 'status': '"+str(response.json()['status'])+"', 'is_started': "+str(response.json()['is_started'])+", 'author': "+str(response.json()['author'])+", 'assigned': "+str(response.json()['assigned'])+"}, 'Comments : ', [OrderedDict([('id', "+str(response1.json()['id'])+"), ('text', '"+str(response1.json()['text'])+"'), ('author', "+str(response1.json()['author'])+"), ('task', "+str(response1.json()['task'])+")])]]"
        self.assertEqual(v, s)
        json.dumps()