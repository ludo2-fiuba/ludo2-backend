from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Attendance, AttendanceQRCode
from backend.permissions import *
from backend.views.base_view import BaseViewSet
from backend.serializers.attendance_serializer import AttendancePostSerializer, AttendanceSerializer
from backend.views.utils import is_before_current_datetime

class AttendanceViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Attendance.objects.all()
    serializer_class = AttendancePostSerializer

    @swagger_auto_schema(
        tags=["Attendances"],
        operation_summary="Submit an attendance"
    )
    def create(self, request):
        attendance_qr_code = get_object_or_404(AttendanceQRCode.objects, qrid=request.data['qrid'])
        semester = attendance_qr_code.semester

        if request.user.student not in semester.students.all():
            return Response("Student not in commission", status=status.HTTP_403_FORBIDDEN)

        if is_before_current_datetime(attendance_qr_code.expires_at):
            return Response("QR code has expired", status=status.HTTP_403_FORBIDDEN)

        if self.get_queryset().filter(student=request.user.student, qr_code=attendance_qr_code, semester=semester).first():
            return Response("This QR code has already been scanned", status=status.HTTP_403_FORBIDDEN)

        attendance = Attendance(student=request.user.student, semester=semester, qr_code=attendance_qr_code)
        attendance.save()
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)
        
    # @action(detail=False, methods=['GET'])
    # @swagger_auto_schema(
    #     tags=["Evaluation Submissions"],
    #     operation_summary="Gets the logged in student's evaluation submissions"
    # )
    # def my_evaluations(self, request):

    #     result = self.queryset.filter(student=request.user.student).all()
    #     return Response(EvaluationSubmissionSerializer(result, many=True).data, status.HTTP_200_OK)
