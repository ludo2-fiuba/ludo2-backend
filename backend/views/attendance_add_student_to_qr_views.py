from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Attendance, AttendanceQRCode, Student
from backend.permissions import *
from backend.serializers.attendance_serializer import (
    AttendanceAddStudentPostSerializer, AttendanceSerializer)
from backend.views.base_view import BaseViewSet
from backend.views.utils import teacher_not_in_commission_staff


class AttendanceAddStudentToQRViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceAddStudentPostSerializer

    @swagger_auto_schema(
        tags=["Attendances"],
        operation_summary="Create an attendance for a QR code"
    )
    def create(self, request):
        attendanceQRCode = get_object_or_404(AttendanceQRCode.objects, qrid=request.data['qrid'])
        student = get_object_or_404(Student.objects, user__id=request.data["student"])
        teacher = request.user.teacher

        commission = attendanceQRCode.semester.commission
        if teacher_not_in_commission_staff(teacher, commission):
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)
        
        if student not in attendanceQRCode.semester.students.all():
            return Response("Student not in commission", status=status.HTTP_403_FORBIDDEN)
        
        attendance = Attendance.objects.filter(qr_code=attendanceQRCode, student=student).first()
        if attendance:
            return Response("Attendance already exists", status=status.HTTP_403_FORBIDDEN)

        attendance = Attendance(semester=attendanceQRCode.semester, student=student, qr_code=attendanceQRCode)
        attendance.save()
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)
    