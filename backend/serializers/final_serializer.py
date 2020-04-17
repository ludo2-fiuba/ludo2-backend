from rest_framework import serializers

from backend.models import Final
from .final_exam_serializer import ApprovedFinalExamSerializer, FinalExamTeacherDetailsSerializer


class ApprovedFinalsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context["filters"]))
        return super(ApprovedFinalsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, filter_params):
        return dict({Final.ALLOWED_FILTERS[key]: value for key, value in filter_params.items() if key in Final.ALLOWED_FILTERS})

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
