from rest_framework.exceptions import APIException


class InvalidImageError(APIException):
    status_code = 400
    default_code = 'invalid_image'


class ErrorCommunicatingWithExternalSourceError(APIException):
    status_code = 500
    default_code = 'communication_error'

    def __init__(self, status_code, **kwargs):
        super().__init__(**kwargs)
        self.status_code = status_code


class InvalidDataError(APIException):
    status_code = 422
    default_code = 'invalid_data'

# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#
#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data['status_code'] = response.status_code
#
#     return response
