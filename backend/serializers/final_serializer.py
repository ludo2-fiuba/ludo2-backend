from rest_framework import serializers

from backend.models import Final
from .filterable_model_list_serializer import FilterableModelListSerializer
from .final_exam_serializer import ApprovedFinalExamSerializer, FinalExamTeacherDetailsSerializer


class FinalsListSerializer(FilterableModelListSerializer):
    MODEL = Final

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context["filters"])).distinct()
        return super(FinalsListSerializer, self).to_representation(data)


class FinalSerializer(serializers.ModelSerializer):
    final_exams = ApprovedFinalExamSerializer(many=True)

    class Meta:
        model = Final
        list_serializer_class = FinalsListSerializer
        fields = ('id', 'date', 'final_exams')


class FinalTeacherSerializer(serializers.ModelSerializer):
    final_exams = FinalExamTeacherDetailsSerializer(many=True)

    class Meta:
        model = Final
        fields = ('id', 'subject', 'date', 'final_exams', 'status')


class FinalSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Final
        fields = ('id', 'date')
