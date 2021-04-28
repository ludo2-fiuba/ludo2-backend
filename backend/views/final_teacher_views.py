from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer, FinalTeacherListSerializer
from backend.services.final_service import FinalService
from backend.services.image_validator_service import ImageValidatorService
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond, validate_face


class FinalTeacherViewSet(BaseViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request):
        finals = self.queryset.filter(teacher=request.user.teacher, subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self._paginate(finals, FinalTeacherListSerializer))

    def create(self, request):
        final = Final(
            subject_siu_id=request.data['subject_siu_id'],
            subject_name=request.data['subject_name'],
            date=datetime.utcfromtimestamp(request.data['timestamp']),
            teacher=request.user.teacher,
            status=Final.Status.DRAFT)
        final.save()
        return respond(self.get_serializer(final), response_status=status.HTTP_201_CREATED)

    def detail(self, request, pk=None):
        return respond(self.get_serializer( get_object_or_404(Final.objects, teacher=request.user.teacher, id=pk)))

    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        final = self._get_final(request.user.teacher, pk, Final.Status.OPEN)
        FinalService().close(final)
        return respond(self.get_serializer(final))

    @action(detail=True, methods=['PUT'])
    def grade(self, request, pk):
        final = self._get_final(request.user.teacher, pk, Final.Status.PENDING_ACT)
        FinalService().grade(final, request.data['grades'])
        return respond(self.get_serializer(final))

    @action(detail=True, methods=['POST'])
    def send_act(self, request, pk):
        validate_face(request, request.user.teacher)

        final = self._get_final(request.user.teacher, pk, Final.Status.PENDING_ACT)
        FinalService().send_act(final)

        return respond(self.get_serializer(final))

    def _get_final(self, teacher, pk, status):
        return get_object_or_404(Final.objects, teacher=teacher, id=pk, status=status)
