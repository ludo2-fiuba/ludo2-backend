from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.services.image_validator_service import ImageValidatorService
from backend.services.siu_service import SiuService
from backend.models import FinalExam, Final
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer
from backend.views.base_view import BaseViewSet


class FinalExamStudentViewSet(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    @action(detail=False, methods=['POST'])
    def take_exam(self, request):
        final = get_object_or_404(Final.objects, qrid=request.data['final'])

        is_match = ImageValidatorService(request.data['photo']).validate_identity(request.user.student)

        if not is_match:
            return Response(status=status.HTTP_403_FORBIDDEN)

        fe = FinalExam(student=request.user.student, final=final)
        serializer = FinalExamSerializer(fe)
        serializer.validate()
        fe.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def history(self, request):
        self.extra = {"grade_gte": FinalExam.PASSING_GRADE, "student": request.user.id}
        return Response(self._group_by(self._paginate(self.queryset), 'subject'))

    @action(detail=False, methods=["GET"])
    def pending(self, request):
        self.extra = {"student": request.user.id}
        subjects_passed = [x.subject for x in self.queryset.annotate(subject=F('final__subject_name')).filter(grade__gte=FinalExam.PASSING_GRADE, student=request.user.id)]
        return Response(self._group_by(self._paginate(self.queryset.exclude(final__subject_name__in=subjects_passed)), 'subject'))

    @ action(detail=True, methods=["GET"])
    def correlatives(self, request, pk):
        self.extra = {}
        fe = get_object_or_404(FinalExam.objects, id=pk, student=request.user.student)
        result = SiuService().correlative_subjects(fe.final.subject_siu_id)
        return Response(self._paginate(self.queryset.filter(final__subject_name__in=[subject['name'] for subject in result], student=request.user.id)))

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def _group_by(self, data, field):
        import itertools
        return {k: list(group) for k, group in itertools.groupby(data, lambda x: x[field])}

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
