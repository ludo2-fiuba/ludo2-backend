from rest_framework import serializers

from backend.models import EvaluationSubmission

from .evaluation_serializer import EvaluationSerializer
from .student_serializer import StudentSerializer
from .teacher_serializer import TeacherSerializer


class EvaludationSubmissionSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer()
    student = StudentSerializer()
    grade = serializers.IntegerField()
    corrector = TeacherSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = EvaluationSubmission
        fields = ('evaluation', 'student', 'grade', 'corrector', 'created_at', 'updated_at')


class EvaludationSubmissionPutSerializer(serializers.ModelSerializer):

    evaluation = serializers.IntegerField()
    student = serializers.IntegerField()
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
