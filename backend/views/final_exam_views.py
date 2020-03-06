from rest_condition import And, Or
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [Or(And(IsPostRequest, permissions.IsAuthenticated, IsStudent),
                             And(IsPutRequest, permissions.IsAuthenticated, IsTeacher))]

    @action(detail=False, methods=['POST'])
    def rendir(self, request):
        # materia y final = chequear el QR
        # chequear la cara
        self.validate_student_biometric_info()
        fe = FinalExam(student=request.user.student, final_id=request.data['final'])
        fe.save()
        return Response(FinalExamSerializer(fe).data, status=status.HTTP_201_CREATED)

    def validate_student_biometric_info(self):
        """Validates if the student info scanned belongs to the student making the request"""
        pass  # TODO implement face scan validation

    @action(detail=True, methods=['PUT'])
    def calificar(self, request, pk=None):
        fe = FinalExam.objects.get(id=pk, final__teacher=request.user.teacher)
        serializer = self.serializer_class(fe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
