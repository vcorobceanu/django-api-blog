from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS = {
        ('open', ('Opened')),
        ('closed', ('Closed')),
    }

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    status = models.CharField(max_length=32, choices=STATUS, default='open', )

    def __str__(self):
        return self.title

class Comments(models.Model):
    text = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Notification(models.Model):
    assigned = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=399)
    seen = models.BooleanField(default=False)
