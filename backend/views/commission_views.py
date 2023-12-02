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

    def list(self, request, *args, **kwargs):
        result = self.get_queryset()
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def subject_commissions(self, request):
        result = self.get_queryset().filter(subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def teachers(self, request):
        result = TeacherRole.objects.all().filter(commission=request.query_params['commission_id'])
        return Response(TeacherRoleSerializer(result, many=True).data, status.HTTP_200_OK)

