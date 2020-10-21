from requests import Response
from rest_framework import status

from backend.utils import response_error_msg


def respond(result, data=None, err_status=status.HTTP_500_INTERNAL_SERVER_ERROR):
    if result.errors:
        return Response(response_error_msg(result.errors), status=err_status)
    return Response(data=data, status=status.HTTP_200_OK)
