from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.models import Subject
from backend.permissions import IsStudent
from backend.serializers.subject_serializer import SubjectSerializer
from django_filters import rest_framework as filters


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    filter_backends = (filters.DjangoFilterBackend,)
    orderiseeng_fields = '__all__'
    filterset_fields = '__all__'

    @action(detail=False)
    def history(self, request):
        self.extra = {"grade_gte": Subject.PASSING_GRADE, "student": request.user.id}

        return self._serialize(Subject.objects)

    @action(detail=False)
    def pending(self, request):
        self.extra = {"student": request.user.id}
        approved = Subject.objects.filter(final__finalexam__grade__gte=Subject.PASSING_GRADE, final__finalexam__student=request.user.id)

        pending_subjects = Subject.objects.exclude(
            id__in=[sub.id for sub in approved]
        )
        return self._serialize(pending_subjects)

    @action(detail=True)
    def correlatives(self, _, pk=None):
        subject = Subject.objects.get(id=pk)

        return self._serialize(subject.correlatives)

    def _serialize(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return Response(serializer.data)

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
