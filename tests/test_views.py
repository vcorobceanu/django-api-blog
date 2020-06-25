from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from TaskManager.models import Task, Comment, Notification


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Billy', password='Milligan')
        user.save()
        task = Task.objects.create(title='Big', description='Bob', assigned=user, author=user)
        comment = Comment.objects.create(text='text', author=user, task_id=1)
        notification = Notification.objects.create(assigned_id=1, info='Notification info', task_id=1)

    pass

    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('list'))
        self.assertEquals(resp.status_code, 302)

    def test_login_user(self):
        response = self.client.post(reverse('login'), {'username': 'Billy', 'password': 'Milligan'})
        self.assertEquals(response.status_code, 200)

