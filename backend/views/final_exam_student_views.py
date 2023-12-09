from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.api_exceptions import InvalidSubjectCodeError
from backend.model_validators import FinalExamValidator
from backend.models import Final, FinalExam
from backend.permissions import *
from backend.serializers.final_exam_serializer import (
    FinalExamSerializer, FinalExamStudentSerializer)
from backend.services.siu_service import SiuService
from backend.views.base_view import BaseViewSet
from backend.views.utils import validate_face


class FinalExamStudentViewSet(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    extra = {}

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def take_exam(self, request):
        final = get_object_or_404(Final.objects, qrid=request.data['final'], status=Final.Status.OPEN)

        validate_face(request, request.user.student)

        fe = FinalExam(student=request.user.student, final=final)
        FinalExamValidator(fe).validate()
        fe.save()
        return Response(FinalExamSerializer(fe).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def history(self, request):
        self.extra = {"grade_gte": FinalExam.PASSING_GRADE, "student": request.user.id, "status__in": [Final.Status.ACT_SENT, Final.Status.PENDING_ACT]}
        return Response(self._paginate(self.get_queryset()))

    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def pending(self, request):
        self.extra = {"student": request.user.id, }
        subjects_passed = [x.subject for x in self.get_queryset().annotate(subject=F('final__subject_name')).filter(grade__gte=FinalExam.PASSING_GRADE, student=request.user.id)]
        return Response(self._paginate(self.get_queryset().exclude(final__subject_name__in=subjects_passed), FinalExamStudentSerializer))

    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def correlatives(self, request):
        self.extra = {}
        subject_code = self.request.query_params.get('code')
        response = SiuService().list_subjects({'codigo': subject_code})

        if not response:
            raise InvalidSubjectCodeError()

        result = SiuService().correlative_subjects(response[0])
        return Response(self._paginate(self.get_queryset().filter(final__subject_siu_id__in=[subject['id'] for subject in result], student=request.user.id, final__status=Final.Status.ACT_SENT, grade__gte=FinalExam.PASSING_GRADE)))

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def _group_by(self, data, field):
        import itertools
        return {k: list(group) for k, group in itertools.groupby(data, lambda x: x[field]['name'])}

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
