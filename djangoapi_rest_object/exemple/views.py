from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from django.db import models

from exemple.models import Car
from rest_object.views import action


class CarSerializer(serializers.ModelSerializer):
    #tags = TagSerializer(many=True)
    id = models.IntegerField(default=1)

    class Meta:
        model = Car
        fields = ('id', 'name', 'maxspeed')

    def update(self, instance, validated_data):
        r = self.create_car(instance, validated_data)
        r.save()
        return instance

    def create(self, validated_data, user=None):
        r = Car()
        # r.user = user
        self.create_car(r, validated_data)
        r.save()
        return r

    def create_car(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.maxspeed = validated_data.get('maxspeed')
        return instance


def car(request, id_car=None, cursor=None, amount=None):
    return action(request, Car, CarSerializer, id_car, cursor, amount)

