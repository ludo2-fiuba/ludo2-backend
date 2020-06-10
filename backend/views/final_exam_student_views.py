from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalStudentExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    @action(detail=False, methods=['POST'])
    def rendir(self, request):
        final_id = self._info_from_qr(request)

        self.validate_ability_to_rendir(request.user.student, final_id)

        self.validate_student_biometric_info()

        fe = FinalExam(student=request.user.student, final_id=final_id)
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

    def _info_from_qr(self, request):
        return request.data['final']

    def validate_student_biometric_info(self):
        """Validates if the student info scanned belongs to the student making the request"""
        pass  # TODO implement face scan validation

    def validate_ability_to_rendir(self, student, final):
        return self._validate_with_siu(student, final)

    def _validate_with_siu(self, student, final):
        return True # TODO call real SIU

    def _serialize(self, relation):
        page = self.paginate_queryset(relation)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relation, many=True)
        import itertools
        return Response({k: list(group) for k, group in itertools.groupby(serializer.data, lambda x: x['subject'])})

    def _filter_params(self):
        return dict({key: value for key, value in self.request.query_params.items()})

    def get_serializer_context(self):
        filter_params = {"filters": dict(self._filter_params(), **self.extra)}
        return dict(super().get_serializer_context(), **filter_params)
