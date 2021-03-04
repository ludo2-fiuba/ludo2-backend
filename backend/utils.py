import base64

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

IMAGE_EXTENSION = 'jpg'


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


def decode_image(b64_image):
    b64_image = b64_image.replace("data:image/jpeg;base64,", "")
    return base64.b64decode(b64_image + "========")


def encode_image(io_object):
    return base64.b64encode(io_object.tobytes())


def user_image_path(dni):
    return f"{dni}.{IMAGE_EXTENSION}"


def response_error_msg(message, code="invalid"):
    return {"message": message, "code": code}
