from rest_framework import serializers

from backend.models import Evaluation

from .semester_serializer import SemesterSerializer


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    semester = SemesterSerializer()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('evaluation_name', 'semester', 'passing_grade', 'start_date', 'end_date')
