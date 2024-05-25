from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import CommissionInscription, Semester, Student
from backend.permissions import *
from backend.serializers.commissionInscription_serializer import (
    CommissionInscriptionPostSerializer, CommissionInscriptionSerializer)
from backend.services.audit_log_service import AuditLogService
from backend.views.base_view import BaseViewSet
from backend.views.utils import teacher_not_in_commission_staff


class CommissionInscriptionTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = CommissionInscription.objects.all()
    serializer_class = CommissionInscriptionPostSerializer

    @swagger_auto_schema(
        tags=["Inscriptions"],
        operation_summary="Gets all semesters the logged in student was inscripted in"
    )
    @action(detail=False, methods=["POST"])
    def add_student(self, request):

        semester = get_object_or_404(Semester.objects, id=request.data["semester"])

        student = get_object_or_404(Student.objects, user__id=request.data["student"])

        if(student in semester.students.all()):
            return Response("Student already in commission", status=status.HTTP_400_BAD_REQUEST)
        
        commission = semester.commission

        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)
        
        commission_inscription = CommissionInscription(student=student, semester=semester, status='A')
        commission_inscription.save()

        AuditLogService().log(request.user, student.user, f"Teacher added sudent to semester.")

        return Response(CommissionInscriptionSerializer(commission_inscription).data, status=status.HTTP_200_OK)
