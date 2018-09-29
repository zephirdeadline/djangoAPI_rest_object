from rest_framework import status


def query(request, Object, ObjectSerializer, cursor, amount, linked_to_user):
    obj = Object.objects.filter(user=request.user) if linked_to_user else Object.objects.all()
    set = ObjectSerializer(obj, many=True).data
    return (set, status.HTTP_200_OK) if cursor is None else (set[int(cursor):int(cursor)+int(amount)], status.HTTP_200_OK)

