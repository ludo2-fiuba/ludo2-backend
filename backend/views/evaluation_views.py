from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation
from backend.serializers.evaluation_serializer import EvaluationSerializer
from backend.views.base_view import BaseViewSet


class EvaluationViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    
    def list(self, request):
        result = self.get_queryset().filter(semester=request.query_params['semester_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
