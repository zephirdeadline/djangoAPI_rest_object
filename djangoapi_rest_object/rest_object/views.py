from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.utils import json


class Log():
    @staticmethod
    def send(arg=None, arg2=None):
        pass


def check_login(func):
    def check(*args, **kwargs):
        try:
            #user = args[0].user
            return func(*args, **kwargs)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(e)}), content_type="application/json", status=401)
    return check


def return_bad_request(error):
    return Response({"status": str(error)}, status=status.HTTP_400_BAD_REQUEST)


def json_from_post(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    return data


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@check_login
def action(request,  Object, serializer=None, id_obj=None):
    if id_obj is not None:
        id_obj = int(id_obj)
    if request.method == "GET":
        if id_obj is None:
            Log.send('GET get list ' + str(type(Object)), request)
            return toList(request, serializer, Object)
        else:
            Log.send('GET get id ' + str(type(Object)), request)
            return get(id_obj, serializer, Object)

    elif request.method == "POST":
        Log.send('POST create', request)
        return create(request, serializer, Object)

    elif request.method == "PUT":
        Log.send('PUT update ' + str(type(Object)), request)
        return update(request, id_obj, serializer, Object)

    elif request.method == "DELETE":
        Log.send('DELETE delete ' + str(type(Object)), request)
        return delete(id_obj, Object)


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
        serializer = serializer(obj, data=json)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)

        return Response({"status": "updated"})
    except Exception as e:
        Log.send('ERROR update ' + str(e))
        return return_bad_request(e)


def create(request, serializer, Object):
    data = json_from_post(request)
    try:
        for json in data:
            serialize = serializer(data=json)
            if serialize.is_valid():
                serialize.create(serialize.validated_data, request.user)

        return Response({"status": "all are saved"})
    except Exception as e:
        Log.send('ERROR create ' + str(e))
        return return_bad_request(e)


def toList(request, serializer, Object):
    serial = serializer(Object.objects.filter(user=request.user), many=True)
    return Response(serial.data)


def get(id_obj, serializer, Object):
    try:
        serial = serializer(Object.objects.get(id=id_obj))
        return Response(serial.data)
    except Exception as e:
        Log.send('ERROR get id')
        return return_bad_request(e)