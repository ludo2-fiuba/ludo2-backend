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
    PASSING_GRADE = 4

    @action(detail=False)
    def approved(self, request):
        approved_subjects = Subject.objects.filter(final__finalexam__grade__gte=self.PASSING_GRADE,
                                                   final__finalexam__student=request.user.id).distinct()

        page = self.paginate_queryset(approved_subjects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(approved_subjects, many=True)
        return Response(serializer.data)
