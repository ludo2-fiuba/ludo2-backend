from rest_framework import serializers

from backend.models import Attendance, AttendanceQRCode

from .semester_serializer import SemesterSerializer
from .student_serializer import StudentSerializer
from .teacher_serializer import TeacherSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    student = StudentSerializer()
    qrid = serializers.UUIDField(source='qr_code.qrid')
    submitted_at = serializers.DateTimeField()

    class Meta:
        model = Attendance
        fields = ('semester', 'student', 'qrid', 'submitted_at')


class AttendancePostSerializer(serializers.ModelSerializer):
    qrid = serializers.UUIDField()

    class Meta:
        model = Attendance
        fields = ('qrid',)


class AttendanceQRCodeSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    owner_teacher = TeacherSerializer()
    created_at = serializers.DateTimeField()
    qrid = serializers.UUIDField()

    class Meta:
        model = AttendanceQRCode
        fields = ('semester', 'owner_teacher', 'created_at', 'qrid')


class AttendanceQRCodePostSerializer(serializers.ModelSerializer):
    semester = serializers.IntegerField()

    class Meta:
        model = AttendanceQRCode
        fields = ('semester',)
