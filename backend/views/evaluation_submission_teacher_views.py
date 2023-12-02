from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.model_validators.EvaluationSubmissionValidator import \
    EvaluationSubmissionValidator
from backend.models import Evaluation, EvaluationSubmission
from backend.permissions import *
from backend.serializers.evaluation_submission_serializer import (
    EvaludationSubmissionCorrectionSerializer, EvaludationSubmissionSerializer)
from backend.views.base_view import BaseViewSet


class EvaluationSubmissionTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = EvaluationSubmission.objects.all()
    serializer_class = EvaludationSubmissionSerializer
        
    @action(detail=False, methods=['GET'])
    def get_submissions(self, request):

        evaluation = get_object_or_404(Evaluation.objects, id=request.query_params["evaluation"])

        if(request.user.teacher not in evaluation.semester.commission.teachers.all()) and (evaluation.semester.commission.chief_teacher != request.user.teacher):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        result = self.queryset.filter(evaluation=request.query_params['evaluation']).all()
        return Response(EvaludationSubmissionCorrectionSerializer(result, many=True).data, status.HTTP_200_OK)