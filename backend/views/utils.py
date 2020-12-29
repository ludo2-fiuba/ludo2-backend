from rest_framework import status
from rest_framework.response import Response


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
