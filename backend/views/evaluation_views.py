from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation
from backend.permissions import *
from backend.serializers.evaluation_serializer import (
    EvaluationSemesterSerializer, EvaluationSerializer)
from backend.views.base_view import BaseViewSet


class EvaluationViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    
    
    @swagger_auto_schema(
        tags=["Evaluations"],
        operation_summary="Gets evaluations from a semester",
        manual_parameters=[
            openapi.Parameter('semester_id', openapi.IN_QUERY, description="Id of semester to get evaluations from", type=openapi.FORMAT_INT64)
        ]
    )
    def list(self, request):
        result = self.get_queryset().filter(semester=request.query_params['semester_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    

    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Evaluations"],
        operation_summary="Gets evaluations from semesters in which the logged in student student in inscripted in"
    )
    def mis_examenes(self, request):
        result = self.queryset.filter(semester__students=request.user.student).all()
        return Response(EvaluationSemesterSerializer(result, many=True).data, status.HTTP_200_OK)
