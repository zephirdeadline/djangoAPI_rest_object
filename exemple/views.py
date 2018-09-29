from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from django.db import models

from exemple.models import Car, CarUser
from rest_object.view import action


class CarUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CarUser
        fields = ('id', 'name', 'maxspeed')

    def update(self, instance, validated_data):
        car = CarUser.objects.filter(id=instance.id)
        car.update(**validated_data)
        return CarUser.objects.get(id=instance.id)

    def create(self, validated_data, user=None):
        car = CarUser.objects.create(user=user, **validated_data)
        return car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'maxspeed')

    def update(self, instance, validated_data):
        car = Car(id=instance.id, **validated_data)
        car.save()
        return car

    def create(self, validated_data, user=None):
        car = Car.objects.create(**validated_data)
        return car


def car(request, id_car=None, cursor=None, amount=None):
    return action(request, Car, CarSerializer, id_car, cursor, amount, is_restricted=False, linked_to_user=False)


def carwithauth(request, id_car=None, cursor=None, amount=None):
    return action(request, Car, CarSerializer, id_car, cursor, amount, is_restricted=True, linked_to_user=False)


def caruser(request, id_car=None, cursor=None, amount=None):
    return action(request, CarUser, CarUserSerializer, id_car, cursor, amount, is_restricted=True, linked_to_user=True)

