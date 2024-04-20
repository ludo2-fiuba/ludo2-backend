from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Attendance, AttendanceQRCode, Semester
from backend.permissions import *
from backend.serializers.attendance_serializer import (
    AttendanceQRCodePostSerializer, AttendanceQRCodeSerializer,
    AttendanceQRCodeStudentsSerializerNoSemester)
from backend.views.base_view import BaseViewSet
from backend.views.utils import teacher_not_in_commission_staff


class AttendanceTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceQRCodePostSerializer

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        tags=["Attendance QRs"],
        operation_summary="Create an attendance QR code"
    )
    def qr(self, request):
        semester = get_object_or_404(Semester.objects, id=request.data['semester'])
        owner_teacher = request.user.teacher

        commission = semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        attendance_qr = AttendanceQRCode(semester=semester, owner_teacher=owner_teacher)
        attendance_qr.save()
        return Response(AttendanceQRCodeSerializer(attendance_qr).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        tags=["Attendance QRs"],
        operation_summary="Get latest valid QR code or create new one"
    )
    def latest_qr(self, request):
        semester = get_object_or_404(Semester.objects, id=request.data['semester'])
        owner_teacher = request.user.teacher

        commission = semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        valid_qr = semester.attendance_qrs.filter(
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if valid_qr:
            return Response(AttendanceQRCodeSerializer(valid_qr).data, status=status.HTTP_200_OK)
        else:
            attendance_qr = AttendanceQRCode(semester=semester, owner_teacher=owner_teacher)
            attendance_qr.save()
            return Response(AttendanceQRCodeSerializer(attendance_qr).data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        tags=["Attendances"],
        operation_summary="Get attendances for a semester"
    )
    def list(self, request):
        semester = get_object_or_404(Semester.objects, id=request.query_params['semester_id'])

        commission = semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        attendances = AttendanceQRCode.objects.filter(semester=semester).all()

        return Response(AttendanceQRCodeStudentsSerializerNoSemester(attendances, many=True).data, status.HTTP_200_OK)
