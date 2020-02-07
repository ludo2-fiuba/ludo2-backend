from rest_framework import serializers

from backend.models import Final
from .final_exam_serializer import FinalExamSerializer


class ApprovedFinalsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(finalexam__grade__gte=4,
                           finalexam__student=self.context['request'].user.id).distinct()
        return super(ApprovedFinalsByStudentListSerializer, self).to_representation(data)


class FinalSerializer(serializers.ModelSerializer):
    final_exams = FinalExamSerializer(source='finalexam_set', many=True)

    class Meta:
        model = Final
        list_serializer_class = ApprovedFinalsByStudentListSerializer
        fields = ('id', 'date', 'final_exams')
