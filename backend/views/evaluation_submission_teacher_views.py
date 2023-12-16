from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation, EvaluationSubmission
from backend.permissions import *
from backend.serializers.evaluation_submission_serializer import (
    EvaluationSubmissionCorrectionSerializer,
    EvaluationSubmissionPutSerializer, EvaluationSubmissionSerializer)
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_datetime


class EvaluationSubmissionTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = EvaluationSubmission.objects.all()
    serializer_class = EvaluationSubmissionPutSerializer
        
    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Gets submissions for an evaluation",
        manual_parameters=[
            openapi.Parameter('evaluation', openapi.IN_QUERY, description="Id of evaluation to get submissions from", type=openapi.FORMAT_INT64)
        ]
    )
    def get_submissions(self, request):

        evaluation = get_object_or_404(Evaluation.objects, id=request.query_params["evaluation"])

        commission = evaluation.semester.commission
        if(request.user.teacher not in commission.teachers.all()) and (commission.chief_teacher != request.user.teacher):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        result = self.queryset.filter(evaluation=request.query_params['evaluation']).all()
        return Response(EvaluationSubmissionCorrectionSerializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Grades an evaluation submission"
    )
    def grade(self, request):
        grade = request.data['grade']
        submission = self.queryset.filter(student__user__id=request.data['student'], evaluation__id=request.data['evaluation']).first()

        if not submission:
            return Response("Submission not found", status=status.HTTP_404_NOT_FOUND)
        
        commission = submission.evaluation.semester.commission
        if(request.user.teacher not in commission.teachers.all()) and (commission.chief_teacher != request.user.teacher):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        submission.grade = grade
        submission.corrector = request.user.teacher
        submission.updated_at = get_current_datetime()
        submission.save()
        return Response(EvaluationSubmissionSerializer(submission).data, status=status.HTTP_200_OK)