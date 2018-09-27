from rest_framework import status

from rest_object.tools.json import parse_json


def update(request, Object, ObjectSerializer, id_object, linked_to_user):
    data = parse_json(request.body)

    serialize = ObjectSerializer(data=data)
    if serialize.is_valid():
        query = Object.objects.get(id=id_object, user=request.user) if linked_to_user else Object.objects.get(id=id_object)
        obj = serialize.update(query, serialize.validated_data)
    else:
        return serialize.errors, status.HTTP_400_BAD_REQUEST
    return ObjectSerializer(obj).data, status.HTTP_200_OK
