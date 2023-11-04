from rest_framework import serializers

from backend.models import CommissionInscription

from .semester_serializer import SemesterSerializer
from .student_serializer import StudentSerializer


class CommissionInscriptionSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    student = StudentSerializer()
    status = serializers.CharField()

    class Meta:
        model = CommissionInscription
        fields = ('semester', 'student', 'status')
