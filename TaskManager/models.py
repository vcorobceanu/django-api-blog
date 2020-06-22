from django.db import models


class MyUser(models.Model):
    name = models.CharField(max_length=20)
    pren = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    passw = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.login


class Task(models.Model):
    STATUS = {
        ('open', ('Opened')),
        ('closed', ('Closed')),
    }

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    assigned = models.CharField(max_length=30, db_index=True)
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default='open',
    )

    def __str__(self):
        return self.title
