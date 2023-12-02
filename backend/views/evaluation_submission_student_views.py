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
    EvaludationSubmissionPostSerializer, EvaludationSubmissionSerializer)
from backend.views.base_view import BaseViewSet


class EvaluationSubmissionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = EvaluationSubmission.objects.all()
    serializer_class = EvaludationSubmissionPostSerializer
        
    @action(detail=False, methods=['POST'])
    def submit_evaluation(self, request):
        
        evaluation = get_object_or_404(Evaluation.objects, id=request.data["evaluation"])

        if(request.user.id != request.data["student"]):
            return Response("Cannot post evaluation for another student", status=status.HTTP_403_FORBIDDEN)

        if(request.user.student not in evaluation.semester.students.all()):
            return Response("Student not in commission", status=status.HTTP_403_FORBIDDEN)

        submission = EvaluationSubmission(student=request.user.student, evaluation=evaluation)
        EvaluationSubmissionValidator(submission).validate()
        submission.save()
        return Response(EvaludationSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)