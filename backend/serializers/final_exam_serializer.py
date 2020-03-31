from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.models import FinalExam
from backend.serializers import StudentSerializer


class ApprovedFinalExamsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(grade__gte=4,
                           student=self.context['request'].user.student).distinct()
        return super(ApprovedFinalExamsByStudentListSerializer, self).to_representation(data)


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
