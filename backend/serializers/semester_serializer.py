from rest_framework import serializers

from backend.models import Semester

from .commission_serializer import CommissionSerializer
from .evaluation_serializer import EvaluationSerializer
from .student_serializer import StudentSerializer


class SemesterSerializer(serializers.ModelSerializer):
    year_moment = serializers.CharField()
    start_date = serializers.DateTimeField()
    commission = CommissionSerializer()
    evaluations = EvaluationSerializer(many=True)
    students = StudentSerializer(many=True)
    classes_amount = serializers.IntegerField()
    minimum_attendance = serializers.FloatField()

    class Meta:
        model = Semester
        fields = ('id', 'year_moment', 'start_date', 'commission', 'evaluations', 'students', 'classes_amount', 'minimum_attendance')
