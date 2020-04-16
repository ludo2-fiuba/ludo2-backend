from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.filters.final_exam_filter import FinalExamFilter
from backend.models import FinalExam, Subject
from backend.serializers import StudentSerializer


class ApprovedFinalExamsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(grade__gte=Subject.PASSING_GRADE,
                           student=self.context['request'].user.student).distinct()
        data = FinalExamFilter(data, self._filter_params(self.context['request'])).filter()
        return super(ApprovedFinalExamsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, request):
        return request.query_params


class FinalExamsListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return super(FinalExamsListSerializer, self).to_representation(data)


class ApprovedFinalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalExam
        list_serializer_class = ApprovedFinalExamsByStudentListSerializer
        fields = ('id', 'student', 'grade')


class FinalExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalExam
        fields = ('id', 'student', 'grade', 'final')
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['list', 'position']
            )
        ]


class FinalExamTeacherDetailsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FinalExam
        list_serializer_class = FinalExamsListSerializer
        fields = ('id', 'student', 'grade')
