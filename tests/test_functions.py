from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from TaskManager.models import Task, Comment, Notification
from TaskManager.notes_fuctions import add_not, notes_count
from TaskManager.timer_functions import *


class FunctionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Billy', password='Milligan')
        cls.task = Task.objects.create(title='Big', description='Bob', assigned_id=1, author_id=1)
        comment = Comment.objects.create(text='text', author_id=1, task_id=1)
        notification = Notification.objects.create(assigned_id=1, info='Notification info', task_id=1)

    def test_add_not(self):
        response = add_not(self.user, 'info', self.task)
        print(response)
