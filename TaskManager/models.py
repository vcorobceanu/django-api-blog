from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS = {
        ('open', 'Opened'),
        ('closed', 'Closed'),
    }

    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    status = models.CharField(max_length=32, choices=STATUS, default='open', )
    is_started = models.BooleanField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Notification(models.Model):
    assigned = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=399)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)