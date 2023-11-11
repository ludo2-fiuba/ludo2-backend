from rest_framework import serializers

from backend.models import Semester

from .commission_serializer import CommissionSerializer
from .evaluation_serializer import EvaluationSerializer


class SemesterSerializer(serializers.ModelSerializer):
    year_moment = serializers.CharField()
    start_date = serializers.DateTimeField()
    commission = CommissionSerializer()
    evaluations = EvaluationSerializer(many=True)

    class Meta:
        model = Semester
        fields = ('year_moment', 'start_date', 'commission', 'evaluations')
