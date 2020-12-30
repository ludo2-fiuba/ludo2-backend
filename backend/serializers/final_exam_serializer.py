from rest_framework import serializers

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
        fields = ('id', 'subject', 'student', 'grade', 'date', 'final')
        list_serializer_class = FinalExamsListSerializer

    def validate(self):
        try:
            FinalExam.objects.get(final=self.data['final'], student=self.data['student'])
        except FinalExam.DoesNotExist:
            return
        raise serializers.ValidationError('field1 with field2 already exists')


class FinalExamTeacherDetailsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FinalExam
        list_serializer_class = FinalExamsListSerializer
        fields = ('id', 'student', 'grade')
