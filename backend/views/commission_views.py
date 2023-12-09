from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Commission, TeacherRole
from backend.serializers.commission_serializer import CommissionSerializer
from backend.serializers.teacher_role_serializer import TeacherRoleSerializer
from backend.views.base_view import BaseViewSet


class CommissionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer

    #def list(self, request, *args, **kwargs):
    #    result = SiuService().list_commissions(request.user.teacher.siu_id)
    #    return respond_plain(result)

    
    @swagger_auto_schema(
        tags=["Commissions"],
        operation_summary="Gets all commissions"
    )
    def list(self, request, *args, **kwargs):
        result = self.get_queryset()
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Commissions"],
        operation_summary="Gets all commissions for a subject",
        manual_parameters=[
            openapi.Parameter('subject_siu_id', openapi.IN_QUERY, description="Id of subject to get commission from", type=openapi.FORMAT_INT64)
        ]
    )
    def subject_commissions(self, request):
        result = self.get_queryset().filter(subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Commissions"],
        operation_summary="Gets all teachers for a commission",
        manual_parameters=[
            openapi.Parameter('commission_id', openapi.IN_QUERY, description="Id of commission to get teachers from", type=openapi.FORMAT_INT64)
        ]
    )
    def teachers(self, request):
        result = TeacherRole.objects.all().filter(commission=request.query_params['commission_id'])
        return Response(TeacherRoleSerializer(result, many=True).data, status.HTTP_200_OK)

