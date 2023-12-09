from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Commission
from backend.permissions import IsTeacher
from backend.serializers.commission_serializer import CommissionSerializer
from backend.views.base_view import BaseViewSet


class CommissionTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Commissions"],
        operation_summary="Get the commissions the logged in teacher is in"
    )
    def my_commissions(self, request):
        result = self.get_queryset().filter(chief_teacher=request.user.teacher).union(self.get_queryset().filter(teachers=request.user.teacher))
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)

