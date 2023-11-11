from rest_framework import serializers

from backend.models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('evaluation_name', 'passing_grade', 'start_date', 'end_date')
