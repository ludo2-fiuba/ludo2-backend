from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class StudentFinalExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

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
