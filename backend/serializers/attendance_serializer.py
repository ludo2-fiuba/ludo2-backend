from rest_framework import serializers

from backend.models import Attendance

from .semester_serializer import SemesterSerializer
from .student_serializer import StudentSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    student = StudentSerializer()
    submitted_at = serializers.DateTimeField()
    qr_generated_at = serializers.DateTimeField()

    class Meta:
        model = Attendance
        fields = ('semester', 'student', 'submitted_at', 'qr_generated_at')


class AttendancePostSerializer(serializers.ModelSerializer):
    semester = serializers.IntegerField()
    qr_generated_at = serializers.DateTimeField()

    class Meta:
        model = Attendance
        fields = ('semester', 'qr_generated_at')
