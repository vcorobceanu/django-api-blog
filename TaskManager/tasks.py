import logging
from django.contrib.auth.models import User
from config.Celery import app
from TaskManager.models import Notification, Task


@app.task
def send_notifications(assigned, info, task):
    try:
        notification = Notification.objects.create(assigned=assigned, info=info, task=task)
        notification.save()
        logging.warning("Notification sent")
    except assigned.DoesNotExist and task.DoesNotExist:
        logging.warning("User or task not existing")
