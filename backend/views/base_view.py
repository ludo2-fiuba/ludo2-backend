from rest_framework import viewsets
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    def _serialize(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return Response(serializer.data)
        #return Response({k: list(group) for k, group in itertools.groupby(serializer.data, lambda x: x['subject'])})
