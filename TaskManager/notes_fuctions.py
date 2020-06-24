from .models import Notification


def add_not(assigned, info, task):
    noti = Notification.objects.create(assigned=assigned, info=info, task=task)
    noti.save()


def notes_count(request):
    count = Notification.objects.filter(assigned=request.user).filter(seen=False).count
    return count
