from rest_framework import status

from rest_object.tools.json import parse_json


def create(request, ObjectSerializer):
    data = parse_json(request.body)
    saved = []
    fails = []
    for json in data:
        serialize = ObjectSerializer(data=json)
        if serialize.is_valid():
            obj = serialize.create(serialize.validated_data, user=request.user)
            saved.append(ObjectSerializer(obj).data)
        else:
            fails.append({'obejct': json, 'error': serialize.errors})
    return {'saved': saved, 'fails': fails}, status.HTTP_200_OK if len(fails) == 0 else status.HTTP_400_BAD_REQUEST

