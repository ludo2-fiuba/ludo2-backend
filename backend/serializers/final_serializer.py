from rest_framework import serializers

from backend.models import Final, Subject
from .final_exam_serializer import ApprovedFinalExamSerializer, FinalExamTeacherDetailsSerializer
from ..filters.final_filter import FinalFilter


class ApprovedFinalsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(finalexam__grade__gte=Subject.PASSING_GRADE,
                           finalexam__student=self.context['request'].user.student).distinct()
        data = FinalFilter(data, self._filter_params(self.context['request'])).filter()
        return super(ApprovedFinalsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, request):
        return request.query_params


class FinalSerializer(serializers.ModelSerializer):
    final_exams = ApprovedFinalExamSerializer(source='finalexam_set', many=True)

    class Meta:
        model = Final
        list_serializer_class = ApprovedFinalsByStudentListSerializer
        fields = ('id', 'date', 'final_exams')


class FinalTeacherSerializer(serializers.ModelSerializer):
    final_exams = FinalExamTeacherDetailsSerializer(source='finalexam_set', many=True)

    class Meta:
        model = Final
        fields = ('id', 'date', 'final_exams')
