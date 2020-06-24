from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.models import FinalExam
from backend.serializers import StudentSerializer
from backend.serializers.filterable_model_list_serializer import FilterableModelListSerializer


class FinalExamsListSerializer(FilterableModelListSerializer):
    MODEL = FinalExam

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context.get("filters", {}))).distinct()
        return super(FinalExamsListSerializer, self).to_representation(data)


class ApprovedFinalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalExam
        fields = ('id', 'grade')
        list_serializer_class = FinalExamsListSerializer


class FinalExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalExam
        fields = ('id', 'student', 'grade', 'date', 'subject')
        list_serializer_class = FinalExamsListSerializer
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
