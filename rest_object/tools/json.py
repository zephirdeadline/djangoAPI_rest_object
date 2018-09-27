from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser


def parse_json(json):
    stream = BytesIO(json)
    data = JSONParser().parse(stream)
    return data