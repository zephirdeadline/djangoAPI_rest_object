from django.db import models

# Create your models here.


class Car(models.Model):
    maxspeed = models.IntegerField()
    name = models.CharField(max_length=256)