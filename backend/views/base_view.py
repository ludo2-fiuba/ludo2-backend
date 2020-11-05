from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):
    def _paginate(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return serializer.data
