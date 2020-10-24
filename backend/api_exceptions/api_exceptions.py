from rest_framework.exceptions import APIException


class InvalidImageError(APIException):
    status_code = 400
    default_code = 'invalid_image'
