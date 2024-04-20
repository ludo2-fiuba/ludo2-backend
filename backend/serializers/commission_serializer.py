from rest_framework import serializers

from backend.models import Commission

from .teacher_serializer import TeacherSerializer


class CommissionSerializer(serializers.ModelSerializer):
    subject_siu_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    chief_teacher = TeacherSerializer()
    chief_teacher_grader_weight = serializers.FloatField()

    class Meta:
        model = Commission
        fields = ('id', 'subject_siu_id', 'subject_name', 'chief_teacher', 'chief_teacher_grader_weight')


class CommissionPutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    chief_teacher_grader_weight = serializers.FloatField()

    class Meta:
        model = Commission
        fields = ('id', 'chief_teacher_grader_weight')
