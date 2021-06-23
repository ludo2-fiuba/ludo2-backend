from rest_framework import serializers

from backend.models import FinalExam
from backend.serializers import StudentSerializer
from backend.serializers.filterable_model_list_serializer import FilterableModelListSerializer


class FinalExamsListSerializer(FilterableModelListSerializer):
    MODEL = FinalExam

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context.get("filters", {})))
        return super(FinalExamsListSerializer, self).to_representation(data)


class FinalExamsPendingListSerializer(FilterableModelListSerializer):
    MODEL = FinalExam

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context.get("filters", {}))).order_by("final__subject_siu_id").distinct("final__subject_siu_id")
        return super(FinalExamsPendingListSerializer, self).to_representation(data)


class FinalExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalExam
        fields = ('id', 'subject', 'teacher_name', 'student', 'grade', 'date', 'final', 'act')
        list_serializer_class = FinalExamsListSerializer


class FinalExamTeacherDetailsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FinalExam
        list_serializer_class = FinalExamsListSerializer
        fields = ('id', 'student', 'grade', 'correlatives_approved')


class FinalExamStudentSerializer(FinalExamSerializer):
    class Meta:
        model = FinalExam
        fields = ('id', 'subject', 'teacher_name', 'student', 'grade', 'date', 'final', 'act')
        list_serializer_class = FinalExamsPendingListSerializer
