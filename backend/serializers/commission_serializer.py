from rest_framework import serializers

from backend.models import Commission

from .teacher_serializer import TeacherSerializer


class CommissionSerializer(serializers.ModelSerializer):
    subject_siu_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    chief_teacher = TeacherSerializer()

    class Meta:
        model = Commission
        fields = ('subject_siu_id', 'subject_name', 'chief_teacher')
