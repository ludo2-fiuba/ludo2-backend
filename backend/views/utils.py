from rest_framework import status
from rest_framework.response import Response


def respond(result, response_status=status.HTTP_200_OK):
    return Response(result.data, status=response_status)
