from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Commission
from backend.serializers.commission_serializer import CommissionSerializer
from backend.services.siu_service import SiuService
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond_plain


class CommissionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer

    def list(self, request, *args, **kwargs):
        result = SiuService().list_commissions(request.user.teacher.siu_id)
        return respond_plain(result)
    
    @action(detail=False, methods=["GET"])
    def list_commissions(self, request):
        result = self.get_queryset()
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def list_subject_commissions(self, request):
        result = self.get_queryset().filter(subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)

