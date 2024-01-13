from django.utils.dateparse import parse_datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Attendance, Semester, AttendanceQRCode
from backend.permissions import *
from backend.views.base_view import BaseViewSet
from backend.serializers.attendance_serializer import AttendanceQRCodePostSerializer, AttendanceQRCodeSerializer
from backend.views.utils import get_current_datetime, get_hours_from_current_time

class AttendanceTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceQRCodePostSerializer

    @swagger_auto_schema(
        tags=["Attendance QRs"],
        operation_summary="Create an attendance QR code"
    )
    def create(self, request):
        semester = get_object_or_404(Semester.objects, id=request.data['semester'])
        owner_teacher = request.user.teacher

        commission = semester.commission
        print(commission.teachers.all(), request.user.teacher)
        if request.user.teacher not in commission.teachers.all() and commission.chief_teacher != request.user.teacher:
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        attendance_qr = AttendanceQRCode(semester=semester, owner_teacher=owner_teacher)
        attendance_qr.save()
        return Response(AttendanceQRCodeSerializer(attendance_qr).data, status=status.HTTP_201_CREATED)
        
    # @action(detail=False, methods=['GET'])
    # @swagger_auto_schema(
    #     tags=["Evaluation Submissions"],
    #     operation_summary="Gets the logged in student's evaluation submissions"
    # )
    # def my_evaluations(self, request):

    #     result = self.queryset.filter(student=request.user.student).all()
    #     return Response(EvaluationSubmissionSerializer(result, many=True).data, status.HTTP_200_OK)
