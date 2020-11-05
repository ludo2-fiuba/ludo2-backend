from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.interactors.image_validator_interactor import ImageValidatorInteractor
from backend.interactors.siu_interactor import SiuInteractor
from backend.models import FinalExam, Final
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer
from backend.views.base_view import BaseViewSet


class FinalStudentExamViewSet(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    @action(detail=False, methods=['POST'])
    def take_exam(self, request):
        final = get_object_or_404(Final.objects, qrid=self._info_from_qr(request))

        is_match = ImageValidatorInteractor(request.data['photo']).validate_identity(request.user.student)

        if not is_match:
            return Response(status=status.HTTP_403_FORBIDDEN)

        fe = FinalExam(student=request.user.student, final=final)
        fe.save()
        return Response(FinalExamSerializer(fe).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def history(self, request):
        self.extra = {"grade_gte": FinalExam.PASSING_GRADE, "student": request.user.id}
        return Response(self._group_by(self._paginate(self.queryset), 'subject'))

    @action(detail=False, methods=["GET"])
    def pending(self, request):
        self.extra = {"student": request.user.id}
        subjects_passed = [x.subject for x in self.queryset.annotate(subject=F('final__subject')).filter(grade__gte=FinalExam.PASSING_GRADE, student=request.user.id)]
        return Response(self._group_by(self._paginate(self.queryset.exclude(final__subject__in=subjects_passed)), 'subject'))

    @ action(detail=True, methods=["GET"])
    def correlatives(self, request, pk):
        fe = get_object_or_404(FinalExam.object, id=pk, student=request.user.student)
        result = SiuInteractor().correlative_finals(fe.get_final.siu_id)
        if result.errors:
            return Response(result.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(self._group_by(self._paginate(self.queryset(final__course__subject__in=result.data, student=fe.student)), 'subject'))

    def _info_from_qr(self, request):
        return request.data['final']

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def _group_by(self, data, field):
        import itertools
        return {k: list(group) for k, group in itertools.groupby(data, lambda x: x[field])}

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
