from rest_framework import status
from rest_framework.response import Response



def check_login(func):
    def check(*args, **kwargs):
        if kwargs['is_restricted'] and args[0].user.is_anonymous:
            return Response({"status": "You aren't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(*args, **kwargs)
    return check