from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from backend.models import Subject
from backend.serializers.subject_serializer import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def history(self, request):
        approved_subjects = Subject.objects.filter(final__finalexam__grade__gte=Subject.PASSING_GRADE,
                                                   final__finalexam__student=request.user.id).distinct()

        return self._serialize(approved_subjects)

    @action(detail=False)
    def pending(self, request):
        pending_subjects = Subject.objects.exclude(
            final__finalexam__grade__gte=Subject.PASSING_GRADE).filter(
            final__finalexam__student=request.user.id)
        return self._serialize(pending_subjects)

    @action(detail=True)
    def correlatives(self, request, pk=None):
        subject = self.get_object()
        correlatives = Subject.objects.filter(correlatives=subject.id)

        return self._serialize(correlatives)

    def _serialize(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return Response(serializer.data)
