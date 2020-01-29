from rest_framework import serializers

from backend.models import FinalExam


class ApprovedFinalExamsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(grade__gte=4,
                           student=self.context['request'].user.id).distinct()
        return super(ApprovedFinalExamsByStudentListSerializer, self).to_representation(data)


class FinalExamSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.padron')
    final = serializers.ReadOnlyField(source='final.subject.name')

    class Meta:
        model = FinalExam
        list_serializer_class = ApprovedFinalExamsByStudentListSerializer
        fields = ('id', 'final', 'student', 'grade')
