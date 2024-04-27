from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation, Semester
from backend.serializers.evaluation_serializer import (
    EvaluationPostSerializer, EvaluationSerializer)
from backend.services.notification_service import NotificationService
from backend.views.base_view import BaseViewSet
from backend.views.utils import datetime_format


class EvaluationTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationPostSerializer
    
    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        tags=["Evaluations"],
        operation_summary="Adds an evaluation for a semester"
    )
    def add_evaluation(self, request):
        evaluation_data = request.data
        evaluation_serializer = EvaluationPostSerializer(data=evaluation_data)
        if evaluation_serializer.is_valid():
            semester = self._semester(evaluation_serializer.initial_data["semester_id"])
            if (semester.commission.chief_teacher == request.user.teacher):
                evaluation_serializer.save()
                return Response(evaluation_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _semester(self, semester_pk):
        return get_object_or_404(Semester.objects, id=semester_pk)
    
    @action(detail=False, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Evaluations"],
        operation_summary="Adds an evaluation for a semester"
    )
    def update_evaluation(self, request):
        evaluation_data = request.data
        semester = self._semester(evaluation_data["semester_id"])

        if semester.commission.chief_teacher != request.user.teacher:
            return Response("Teacher not chief teacher in commission", status=status.HTTP_403_FORBIDDEN)

        evaluations = Evaluation.objects.filter(semester=semester).all()

        evaluation = None
        for an_evaluation in evaluations:
            if an_evaluation.evaluation_name == evaluation_data["evaluation_name"]:
                evaluation = an_evaluation

        if not evaluation:
            return Response("Evaluation does not exist", status=status.HTTP_404_NOT_FOUND)
        
        if evaluation_data["passing_grade"]:
            evaluation.passing_grade = evaluation_data["passing_grade"]
        
        if evaluation_data["is_graded"] is not None:
            evaluation.is_graded = evaluation_data["is_graded"]
        
        start_date = datetime_format(evaluation_data["start_date"])
        if start_date:
            evaluation.start_date = start_date
        
        end_date = datetime_format(evaluation_data["end_date"])
        if end_date:
            evaluation.end_date = end_date

        if evaluation.start_date > evaluation.end_date:
            return Response("Start date cannot be after end date", status=status.HTTP_403_FORBIDDEN)

        evaluation.save()

        return Response(EvaluationSerializer(evaluation).data, status=status.HTTP_400_BAD_REQUEST)

    def _semester(self, semester_pk):
        return get_object_or_404(Semester.objects, id=semester_pk)


    @action(detail=True, methods=['POST'])
    @swagger_auto_schema(
        tags=["Evaluations"],
        operation_summary="Notifies grades"
    )
    def notify_grades(self, request, pk=None):

        evaluation = get_object_or_404(Evaluation.objects, id=pk)

        NotificationService().notify_evaluation_grade(evaluation)
