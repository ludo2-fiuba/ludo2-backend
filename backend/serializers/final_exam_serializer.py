from rest_framework import serializers

from backend.models import FinalExam


class ApprovedFinalExamsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(grade__gte=4,
                           student=self.context['request'].user.request).distinct()
        return super(ApprovedFinalExamsByStudentListSerializer, self).to_representation(data)


class ApprovedFinalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalExam
        list_serializer_class = ApprovedFinalExamsByStudentListSerializer
        fields = ('id', 'student', 'grade')


class FinalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalExam
        fields = ('id', 'student', 'grade')
