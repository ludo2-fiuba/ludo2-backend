from rest_framework import serializers

from backend.models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'passing_grade', 'start_date', 'end_date')


class EvaluationPostSerializer(serializers.ModelSerializer):
    semester_id = serializers.IntegerField()
    evaluation_name = serializers.CharField()
    is_graded = serializers.BooleanField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('semester_id', 'evaluation_name', 'is_graded', 'passing_grade', 'start_date', 'end_date')
