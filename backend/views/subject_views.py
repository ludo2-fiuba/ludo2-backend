from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.models import Subject
from backend.permissions import IsStudent
from backend.serializers.subject_serializer import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    @action(detail=False)
    def history(self, request):
        approved_subjects = Subject.objects.filter(final__finalexam__grade__gte=Subject.PASSING_GRADE,
                                                   final__finalexam__student=request.user.id).distinct()

        return self._serialize(approved_subjects)

    @action(detail=False)
    def pending(self, request):
        approved = Subject.objects.filter(final__finalexam__grade__gte=Subject.PASSING_GRADE, final__finalexam__student=request.user.id)

        pending_subjects = Subject.objects.filter(
            final__finalexam__student=request.user.id).exclude(
            id__in=[sub.id for sub in approved]
        )
        return self._serialize(pending_subjects)

    @action(detail=True)
    def correlatives(self, request, pk=None):
        subject = Subject.objects.get(id=pk)

        return self._serialize(subject.correlatives.all())

    def _serialize(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return Response(serializer.data)
