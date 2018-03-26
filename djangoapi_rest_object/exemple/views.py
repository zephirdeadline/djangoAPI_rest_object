from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from exemple.models import Car
from rest_object.views import action


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'name', 'maxspeed')


def save_car_from_json(request, json, car):

    car.maxspeed = json["maxspeed"]
    car.name = json["name"]
    car.save()


def car(request, id_car=None):
    return action(request, Car, CarSerializer, save_car_from_json, id_car)
