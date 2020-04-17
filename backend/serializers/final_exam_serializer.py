from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.models import FinalExam
from backend.serializers import StudentSerializer


class ApprovedFinalExamsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context["filters"]))
        return super(ApprovedFinalExamsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, filter_params):
        return dict({FinalExam.ALLOWED_FILTERS[key]: value for key, value in filter_params.items() if key in FinalExam.ALLOWED_FILTERS})


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
