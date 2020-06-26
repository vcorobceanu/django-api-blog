import time

from celery import shared_task
from .models import Notification

@shared_task(bind=True)
def add_not(assigned, info, task):
    noti = Notification.objects.create(assigned=assigned, info=info, task=task)
    noti.save()
    while True:
    	time.sleep(10)
    	print('test')


def notes_count(request):
    count = Notification.objects.filter(assigned=request.user).filter(seen=False).count
    return count
