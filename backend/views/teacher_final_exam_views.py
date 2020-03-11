from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class TeacherFinalExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['PUT'])
    def calificar(self, request, pk=None):
        fe = FinalExam.objects.get(id=pk, final__teacher=request.user.teacher)
        serializer = self.serializer_class(fe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
