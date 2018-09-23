
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.utils import json
from django.conf import settings
from rest_object.tools.log import Log


def check_login(func):
    def check(*args, **kwargs):
        if settings.REQUIRE_API_AUTHORISATION and args[0].user.is_anonymous:
            return Response({"status": "You aren't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(*args, **kwargs)
    return check


def return_bad_request(error):
    return Response({"status": str(error)}, status=status.HTTP_400_BAD_REQUEST)


def json_from_post(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    return data


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@check_login
def action(request,  Object, serializer, id_obj=None, cursor=None, amount=None):
    if id_obj is not None:
        id_obj = int(id_obj)
    if cursor is not None:
        cursor = int(cursor)
        amount = int(amount)
    if request.method == "GET":
        if id_obj is None:
            if cursor is not None and amount is not None:
                Log.send('GET get list with amount ' + str(type(Object)), request)
                return toListWithAmount(cursor, amount, request, serializer, Object)
            else:
                Log.send('GET get list ' + str(type(Object)), request)
                return toList(request, serializer, Object)
        else:
            Log.send('GET get id ' + str(type(Object)), request)
            return get(id_obj, request, serializer, Object)

    elif request.method == "POST":
        Log.send('POST create', request)
        return create(request, serializer)

    elif request.method == "PUT":
        Log.send('PUT update ' + str(type(Object)), request)
        return update(request, id_obj, serializer, Object)

    elif request.method == "DELETE":
        Log.send('DELETE delete ' + str(type(Object)), request)
        return delete(id_obj, Object)
    else:
        return_bad_request("Bad argument")


def delete(id_obj, Object):
    try:
        Object.objects.get(id=id_obj).delete()
        return Response({"status": "success"})
    except Exception as e:
        Log.send('ERROR delete ' + str(e))
        return return_bad_request(e)


def update(request, id_obj, serializer, Object):
    json = json_from_post(request)
    try:
        obj = Object.objects.get(id=id_obj)
        serialize = serializer(obj, data=json)
        if serialize.is_valid():
            serialize.update(obj, serialize.validated_data)
        else:
            return return_bad_request(serialize.errors)
        return Response({"status": "updated"})
    except Exception as e:
        Log.send('ERROR update ' + str(e))
        return return_bad_request(e)


def create(request, serializer):
    data = json_from_post(request)
    try:
        for json in data:
            serialize = serializer(data=json)
            if serialize.is_valid():
                if serialize.create(serialize.validated_data, user=request.user):
                    return Response({"status": "all are saved"})
                else:
                    return return_bad_request({"status": "Don't respect constraite"})
            else:
                return return_bad_request(serialize.errors)

    except Exception as e:
        Log.send('ERROR create ' + str(e))
        return return_bad_request(e)


def toList(request, serializer, Object):
    if not settings.IS_GLOBAL_DATA:
        serial = serializer(Object.objects.filter(user=request.user), many=True)
    else:
        serial = serializer(Object.objects.all(), many=True)
    return Response(serial.data)



def toListWithAmount(cursor, amount, request, serializer, Object):
    if not settings.IS_GLOBAL_DATA:
        serial = serializer(Object.objects.filter(user=request.user), many=True)
    else:
        serial = serializer(Object.objects.all(), many=True)
    return Response(serial.data[cursor:cursor+amount])



def get(id_obj, request, serializer, Object):
    try:
        if not settings.IS_GLOBAL_DATA:
            serial = serializer(Object.objects.get(user=request.user, id=id_obj))
        else:
            serial = serializer(Object.objects.get(id=id_obj))
        return Response(serial.data)
    except Exception as e:
        Log.send('ERROR get id')
        return return_bad_request(e)
