from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback


def api_exception_handler(exception, context):

    if isinstance(exception, exceptions.APIException):

        headers = {}

        if getattr(exception, 'auth_header', None):
            headers['WWW-Authenticate'] = exception.auth_header

        if getattr(exception, 'wait', None):
            headers['Retry-After'] = '%d' % exception.wait

        data = exception.get_full_details()
        set_rollback()

        return Response(data, status=exception.status_code, headers=headers)

    return exception_handler(exception, context)
