from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    assigned = models.CharField(max_length=30, db_index=True)
