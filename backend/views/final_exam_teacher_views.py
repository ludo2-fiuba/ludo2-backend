from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import FinalExam, Final, Student
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamTeacherDetailsSerializer
from backend.model_validators import FinalExamValidator
from backend.views.base_view import BaseViewSet


class FinalExamTeacherViews(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamTeacherDetailsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['PUT'])
    def grade(self, request, pk=None, final_pk=None):
        serializer = self.get_serializer(self._fe(final_pk, pk, request.user.teacher), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, final_pk=None, *args, **kwargs):
        fe = FinalExam(student=self._student(request.data['padron']), final=self._final(final_pk, request.user.teacher))
        FinalExamValidator(fe).validate()
        fe.save()
        return Response(self.get_serializer(fe).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, final_pk=None, *args, **kwargs):
        fe = self._fe(final_pk, pk, request.user.teacher)
        data = self.get_serializer(fe).data
        fe.delete()
        return Response(data, status=status.HTTP_200_OK)

    def _final(self, final_pk, teacher):
        return get_object_or_404(Final.objects, id=final_pk, teacher=teacher)

    def _fe(self, final_pk, pk, teacher):
        return get_object_or_404(FinalExam.objects, id=pk, final_id=final_pk, final__teacher=teacher, final__status=Final.Status.OPEN)

    def _student(self, padron):
        return get_object_or_404(Student.objects, padron=padron)
