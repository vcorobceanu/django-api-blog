from django.contrib.auth.models import User
from .models import Task, Notification
from celery import shared_task


@shared_task
def add_not(assigned_id, info, task_id):
    assigned = User.objects.get(id=assigned_id)
    task = Task.objects.get(id=task_id)
    noti = Notification.objects.create(assigned=assigned, info=info, task=task)
    noti.save()


def notes_count(request):
    count = Notification.objects.filter(assigned=request.user).filter(seen=False).count()
    return count
