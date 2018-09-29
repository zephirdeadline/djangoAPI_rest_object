from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Car(models.Model):
    maxspeed = models.IntegerField()
    name = models.CharField(max_length=256)


class CarUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maxspeed = models.IntegerField()
    name = models.CharField(max_length=256)