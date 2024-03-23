from rest_framework import serializers

from backend.models import Evaluation, Semester

from .commission_serializer import CommissionSerializer


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    is_graded = serializers.BooleanField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'is_graded', 'passing_grade', 'start_date', 'end_date')


class EvaluationWithMakeupSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    is_graded = serializers.BooleanField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'is_graded', 'passing_grade', 'start_date', 'end_date', 'make_up_evaluation')
    
    def get_fields(self):
        fields = super(EvaluationWithMakeupSerializer, self).get_fields()
        fields['make_up_evaluation'] = EvaluationWithMakeupSerializer()
        return fields


class SemesterEvaluationsSerializer(serializers.ModelSerializer):
    year_moment = serializers.CharField()
    start_date = serializers.DateTimeField()
    commission = CommissionSerializer()

    class Meta:
        model = Semester
        fields = ('id', 'year_moment', 'start_date', 'commission')


class EvaluationSemesterSerializer(serializers.ModelSerializer):
    evaluation_name = serializers.CharField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    semester = SemesterEvaluationsSerializer()


    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'passing_grade', 'start_date', 'end_date', 'semester')


class EvaluationPostSerializer(serializers.ModelSerializer):
    semester_id = serializers.IntegerField()
    evaluation_name = serializers.CharField()
    is_graded = serializers.BooleanField()
    passing_grade = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Evaluation
        fields = ('semester_id', 'evaluation_name', 'is_graded', 'passing_grade', 'start_date', 'end_date')
