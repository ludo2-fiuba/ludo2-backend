from rest_framework import serializers

from backend.models import Course
from backend.serializers import FinalSimpleSerializer


class CourseSerializer(serializers.ModelSerializer):
    finals = FinalSimpleSerializer(many=True)

    class Meta:
        model = Course
        fields = ('subject', 'semester', 'teacher', 'finals')

    def teacher(self):
        return self.obj.teacher()
