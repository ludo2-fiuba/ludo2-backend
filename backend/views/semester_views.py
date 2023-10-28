from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Semester
from backend.serializers.semester_serializer import SemesterSerializer
from backend.services.siu_service import SiuService
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond_plain


class SemesterViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    
    @action(detail=False, methods=["GET"])
    def list_subject_semesters(self, request):
        result = self.get_queryset().filter(commission__subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def list_present_subject_semesters(self, request):
        result = self.get_queryset().filter(commission__subject_siu_id=request.query_params['subject_siu_id'], 
                                            start_date__year__gte=datetime.now().year, year_moment=self._get_semester())
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)

    def _get_semester(self):
        mes = datetime.now().month
        # TODO: hacerlo configurable
        if (mes >= 8) or (mes <= 2):
            return 'SS'
        return 'FS'
        

