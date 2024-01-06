from rest_framework import serializers

from backend.models import TeacherRole

from .commission_serializer import CommissionSerializer
from .teacher_serializer import TeacherSerializer


class TeacherRoleSerializer(serializers.ModelSerializer):
    commission = CommissionSerializer()
    teacher = TeacherSerializer()
    role = serializers.CharField()

    class Meta:
        model = TeacherRole
        fields = ('commission', 'teacher', 'role')


class TeacherRolePostSerializer(serializers.ModelSerializer):
    commission = serializers.IntegerField()
    teacher = serializers.IntegerField()
    role = serializers.CharField()

    class Meta:
        model = TeacherRole
        fields = ('commission', 'teacher', 'role')