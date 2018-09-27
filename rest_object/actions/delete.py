from rest_framework import status


def delete(request, Object, id_object, linked_to_user):
    Object.objects.get(id=id_object, user=request.user).delete() if linked_to_user else Object.objects.get(id=id_object).delete()
    return {'ok'}, status.HTTP_200_OK
