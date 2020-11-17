from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):
    def _paginate(self, relation, serializer=None):
        if not serializer:
            serializer = self.get_serializer
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer(relation, many=True)
        return serializer.data
