from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.interactors.correlative_subjects_lister_interactor import CorrelativeSubjectsListerInteractor
from backend.interactors.final_requirements_validator_interactor import FinalRequirementsValidatorInteractor
from backend.models import FinalExam, Final
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalStudentExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    @action(detail=False, methods=['POST'])
    def rendir(self, request):
        final = get_object_or_404(Final.object, qrid=self._info_from_qr(request))

        result = self._validate_requirements(request.user.student, final.subject())
        if result.errors:
            return Response(result.errors, status=status.HTTP_403_FORBIDDEN)

        self._validate_student_biometric_info()

        fe = FinalExam(student=request.user.student, final=final)
        fe.save()
        return Response(FinalExamSerializer(fe).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def history(self, request):
        self.extra = {"grade_gte": FinalExam.PASSING_GRADE, "student": request.user.id}
        return self._serialize(self.queryset)

    @action(detail=False, methods=["GET"])
    def pending(self, request):
        self.extra = {"student": request.user.id}
        approved_subjects = [x.subject for x in self.queryset.annotate(subject=F('final__course__subject')).filter(grade__gte=FinalExam.PASSING_GRADE, student=request.user.id)]
        return self._serialize(self.queryset.exclude(final__course__subject__in=approved_subjects))

    @action(detail=True, methods=["GET"])
    def correlatives(self, request, pk):
        fe = get_object_or_404(FinalExam.object, id=pk, student=request.user.student)

        result = self._correlative_subjects(fe.subject())
        if result.errors:
            return Response(result.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return self._serialize(self.queryset(final__course__subject__in=result.data, student=fe.student))

    def _info_from_qr(self, request):
        return request.data['final']

    def _validate_student_biometric_info(self):
        """Validates if the student info scanned belongs to the student making the request"""
        pass  # TODO implement face scan validation

    def _validate_requirements(self, student, fe):
        return FinalRequirementsValidatorInteractor(student, fe.subject()).validate()

    def _correlative_subjects(self, subject):
        return CorrelativeSubjectsListerInteractor(subject).list()

    def _serialize(self, relation):
        import itertools
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        return Response({k: list(group) for k, group in itertools.groupby(serializer.data, lambda x: x['subject'])})

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
