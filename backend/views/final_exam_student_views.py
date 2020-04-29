from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import FinalExam, Student
from backend.permissions import *
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalStudentExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    @action(detail=False, methods=['POST'])
    def rendir(self, request):
        final_id = self.info_from_qr(request)

        self.validate_ability_to_rendir(request.user.student, final_id)

        self.validate_student_biometric_info()

        fe = FinalExam(student=request.user.student, final_id=final_id)
        fe.save()
        return Response(FinalExamSerializer(fe).data, status=status.HTTP_201_CREATED)

    def info_from_qr(self, request):
        return request.data['final']

    def validate_student_biometric_info(self):
        """Validates if the student info scanned belongs to the student making the request"""
        pass  # TODO implement face scan validation

    def validate_ability_to_rendir(self, student, final):
        return self._taken_course(student, final)

    def _taken_course(self, student, final):
        return student.courses.filter(subject=final.subject).exists()
