from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import FinalExam, Final
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer
from backend.views.base_view import BaseViewSet


class FinalTeacherExamViews(BaseViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['PUT'])
    def grade(self, request, pk=None):
        serializer = self.serializer_class(self._fe(pk, request.user.teacher), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _fe(self, pk, teacher):
        return get_object_or_404(FinalExam.objects, id=pk, final__teacher=teacher, status=Final.Status.OPEN)
