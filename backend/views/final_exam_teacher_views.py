from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.model_validators import FinalExamValidator
from backend.models import Final, FinalExam, Student
from backend.permissions import *
from backend.serializers.final_exam_serializer import \
    FinalExamTeacherDetailsSerializer
from backend.services.audit_log_service import AuditLogService
from backend.views.base_view import BaseViewSet


class FinalExamTeacherViews(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamTeacherDetailsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def grade(self, request, pk=None, final_pk=None):
        serializer = self.get_serializer(self._fe(final_pk, pk, request.user.teacher), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            AuditLogService().log(request.user, None, f"Teacher graded a final exam: {self._fe(final_pk, pk, request.user.teacher)}")

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def create(self, request, final_pk=None, *args, **kwargs):
        fe = FinalExam(student=self._student(request.data['padron']), final=self._final(final_pk, request.user.teacher))
        FinalExamValidator(fe).validate()
        fe.save()

        AuditLogService().log(request.user, self._student(request.data['padron']).user, f"Teacher graded a final exam: {self._final(final_pk, request.user.teacher)}")
        
        return Response(self.get_serializer(fe).data, status=status.HTTP_201_CREATED)

    
    @swagger_auto_schema(
        tags=["Final Exams"]
    )
    def destroy(self, request, pk=None, final_pk=None, *args, **kwargs):
        fe = self._fe(final_pk, pk, request.user.teacher)
        data = self.get_serializer(fe).data
        fe.delete()
        return Response(data, status=status.HTTP_200_OK)

    def _final(self, final_pk, teacher):
        return get_object_or_404(Final.objects, id=final_pk, teacher=teacher)

    def _fe(self, final_pk, pk, teacher):
        return get_object_or_404(FinalExam.objects, id=pk, final_id=final_pk, final__teacher=teacher, final__status=Final.Status.PENDING_ACT)

    def _student(self, padron):
        return get_object_or_404(Student.objects, padron=padron)
