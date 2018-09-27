from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_object.actions.create import create
from rest_object.actions.delete import delete
from rest_object.actions.get import get
from rest_object.actions.query import query
from rest_object.actions.update import update
from rest_object.tools.check_login import check_login


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@check_login
def action(request,  Object, ObjectSerializer, id_object=None, cursor=None, amount=None, is_restricted=True, linked_to_user=True):
    try:
        if request.method == "GET" and id_object is None:
            result, code = query(request, Object, ObjectSerializer, cursor, amount, linked_to_user)
        elif request.method == "GET":
            result, code = get(request, Object, ObjectSerializer, id_object, linked_to_user)
        elif request.method == "POST":
            result, code = create(request, ObjectSerializer)
        elif request.method == "PUT":
            result, code = update(request, Object, ObjectSerializer, id_object, linked_to_user)
        elif request.method == "DELETE":
            result, code = delete(request, Object, id_object, linked_to_user)
        else:
            return Response({'Request is not supported'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=code)

    except Exception as e:
        return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)


