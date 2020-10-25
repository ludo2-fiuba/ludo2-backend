from requests import Response
from rest_framework import status


def respond(result, response_status=status.HTTP_200_OK):
    return Response(data=result.data, status=response_status)
