from datetime import datetime, timezone

from rest_framework import status
from rest_framework.response import Response

from backend.api_exceptions import InvalidFaceError
from backend.services.image_validator_service import ImageValidatorService


def respond(result, response_status=status.HTTP_200_OK):
    return respond_plain(result.data, response_status=response_status)


def respond_plain(result, response_status=status.HTTP_200_OK):
    return Response(result, status=response_status)


def serialize(self, relation):
    page = self.paginate_queryset(relation)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(relation, many=True)
    return Response(serializer.data)


def validate_face(request, model):
    if not request.data.get('image'):
        raise InvalidFaceError()

    is_match = ImageValidatorService(request.data['image']).validate_identity(model)

    if not is_match:
        return InvalidFaceError()

def get_current_semester():
    mes = datetime.now().month
    # TODO: hacerlo configurable
    if (mes >= 8) or (mes <= 2):
        return 'SS'
    return 'FS'

def get_current_year():
    return 2023

def get_current_datetime():
    return datetime.now(timezone.utc)

def get_hours_from_current_time(past_datetime):
    SECONDS_IN_ONE_HOUR = 3600
    return (get_current_datetime() - past_datetime).total_seconds() / SECONDS_IN_ONE_HOUR
