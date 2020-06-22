from django.db import models

class MyUser(models.Model):
    name = models.CharField(max_length=20)
    pren = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    passw = models.CharField(max_length=20, unique=True)