from rest_framework import serializers

from backend.models import EvaluationSubmission

from .evaluation_serializer import EvaluationSerializer
from .student_serializer import StudentSerializer


class EvaludationSubmissionSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer()
    student = StudentSerializer()
    grade = serializers.IntegerField()

    class Meta:
        model = EvaluationSubmission
        fields = ('evaluation', 'student', 'grade')



class EvaludationSubmissionPostSerializer(serializers.ModelSerializer):

    evaluation = serializers.IntegerField()
    student = serializers.IntegerField()

    class Meta:
        model = EvaluationSubmission
        fields = ('evaluation', 'student')


class EvaludationSubmissionCorrectionSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    grade = serializers.IntegerField()

    class Meta:
        model = EvaluationSubmission
        fields = ('student', 'grade')
