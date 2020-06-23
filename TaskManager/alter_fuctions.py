from .models import Notification

def add_not(assigned, info):
    noti = Notification.objects.create(assigned=assigned, info=info)
    noti.save()