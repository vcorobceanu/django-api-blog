import time

from django.contrib.auth.models import User
from .models import Task
from celery import shared_task
from .models import Notification


@shared_task
def add_not(assigned_id, info, task_id):
    assigned = User.objects.get(id=assigned_id)
    task = Task.objects.get(id=task_id)
    noti = Notification.objects.create(assigned=assigned, info=info, task=task)
    noti.save()


@shared_task
def test_task(duration):
    for x in range(duration):
        print('test')
        time.sleep(10)
    return None