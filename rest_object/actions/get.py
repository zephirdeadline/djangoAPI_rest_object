from rest_framework import status


def get(request, Object, ObjectSerializer, id_object, linked_to_user):
    obj = Object.objects.get(id=id_object, user=request.user) if linked_to_user else Object.objects.get(id=id_object)
    return ObjectSerializer(obj).data, status.HTTP_200_OK
