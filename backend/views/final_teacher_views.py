from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.services.final_service import FinalService
from backend.services.siu_service import SiuService
from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer, FinalTeacherListSerializer
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond, respond_2


class FinalTeacherViewSet(BaseViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request):
        finals = self.queryset.filter(teacher=request.user.teacher, subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self._paginate(finals, FinalTeacherListSerializer))

    def create(self, request):
        siu_final = SiuService().create_final(request.user.teacher.siu_id, request.data['subject_siu_id'], request.data["timestamp"])
        final = Final(
            siu_id=siu_final["id"],
            subject_name=request.data['subject_name'],
            subject_siu_id=request.data['subject_siu_id'],
            date=datetime.utcfromtimestamp(request.data['timestamp']),
            teacher=request.user.teacher)
        final.save()
        return respond(self.get_serializer(final), response_status=status.HTTP_201_CREATED)

    def detail(self, request, pk=None):
        return respond(self.get_serializer(self._get_final(request.user.teacher, pk)))

    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        result = FinalService().close(self._get_final(request.user.teacher, pk))
        return respond(self.get_serializer(result.data))

    @action(detail=True, methods=['POST'])
    def send_act(self, request, pk):
        result = FinalService().send_act(self._get_final(request.user.teacher, pk))
        return respond(self.get_serializer(result.data))

    def _get_final(self, teacher, pk):
        return get_object_or_404(Final.objects, teacher=teacher, id=pk)
