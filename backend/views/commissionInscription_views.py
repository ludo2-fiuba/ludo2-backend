from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import CommissionInscription
from backend.serializers.commissionInscription_serializer import \
    CommissionInscriptionSerializer
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_semester, get_current_year


class CommissionInscriptionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CommissionInscription.objects.all()
    serializer_class = CommissionInscriptionSerializer

    def list(self, request, *args, **kwargs):
        result = self.get_queryset().filter(student=request.user.student)
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def current_inscriptions(self, request):
        allStatus = self.get_queryset().filter(student=request.user.student,
                                            semester__start_date__year__gte=get_current_year(), 
                                            semester__year_moment=get_current_semester())
        result = allStatus.filter(status="A") | allStatus.filter(status="P")
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
