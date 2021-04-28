from rest_framework import serializers

from backend.models import FinalExam, Final
from backend.serializers import StudentSerializer
from backend.serializers.filterable_model_list_serializer import FilterableModelListSerializer


class FinalExamsListSerializer(FilterableModelListSerializer):
    MODEL = FinalExam

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context.get("filters", {}))).distinct()
        return super(FinalExamsListSerializer, self).to_representation(data)


class FinalExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalExam
        fields = ('id', 'subject', 'teacher_name', 'student', 'grade', 'date', 'final')
        list_serializer_class = FinalExamsListSerializer


class FinalExamTeacherDetailsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FinalExam
        list_serializer_class = FinalExamsListSerializer
        fields = ('id', 'student', 'grade', 'correlatives_approved')


class FinalExamStudentSerializer(FinalExamSerializer):
    grade = serializers.SerializerMethodField()

    def get_grade(self, obj):
        return None if obj.final.status != Final.Status.ACT_SENT else obj.grade

    class Meta:
        model = FinalExam
        fields = ('id', 'subject', 'teacher_name', 'student', 'grade', 'date', 'final')
        list_serializer_class = FinalExamsListSerializer
