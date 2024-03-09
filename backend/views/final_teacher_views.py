from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import (FinalTeacherListSerializer,
                                                  FinalTeacherSerializer)
from backend.services.audit_log_service import AuditLogService
from backend.services.final_service import FinalService
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond, validate_face


class FinalTeacherViewSet(BaseViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        tags=["Finals"]
    )
    def list(self, request):
        finals = self.queryset.filter(teacher=request.user.teacher, subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self._paginate(finals, FinalTeacherListSerializer))

    @swagger_auto_schema(
        tags=["Finals"]
    )
    def create(self, request):
        final = Final(
            subject_siu_id=request.data['subject_siu_id'],
            subject_name=request.data['subject_name'],
            date=datetime.utcfromtimestamp(request.data['timestamp']),
            teacher=request.user.teacher,
            status=Final.Status.DRAFT)
        final.save()

        AuditLogService().log(request.user, None, f"Teacher created a final for: {request.data['subject_name']}")

        return respond(self.get_serializer(final), response_status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Finals"]
    )
    def retrieve(self, request, pk=None):
        return respond(self.get_serializer(get_object_or_404(Final.objects, teacher=request.user.teacher, id=pk)))

    @action(detail=True, methods=['POST'])
    @swagger_auto_schema(
        tags=["Finals"]
    )
    def notify_grades(self, request, pk):
        final = self._get_final(request.user.teacher, pk, Final.Status.PENDING_ACT)
        FinalService().notify_grades(final)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Finals"]
    )
    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        final = self._get_final(request.user.teacher, pk, Final.Status.OPEN)
        FinalService().close(final)

        AuditLogService().log(request.user, None, f"Teacher closed a final: {final}")

        return respond(self.get_serializer(final))

    @swagger_auto_schema(
        tags=["Finals"]
    )
    @action(detail=True, methods=['PUT'])
    def grade(self, request, pk):
        final = self._get_final(request.user.teacher, pk, Final.Status.PENDING_ACT)
        FinalService().grade(final, request.data['grades'])

        AuditLogService().log(request.user, None, f"Teacher graded a final: {final}")
        
        return respond(self.get_serializer(final))

    @swagger_auto_schema(
        tags=["Finals"]
    )
    @action(detail=True, methods=['POST'])
    def send_act(self, request, pk):
        validate_face(request, request.user.teacher)

        final = self._get_final(request.user.teacher, pk, Final.Status.PENDING_ACT)
        FinalService().send_act(final)

        AuditLogService().log(request.user, None, f"Teacher closed an act: {final}")

        return respond(self.get_serializer(final))

    @swagger_auto_schema(
        tags=["Finals"]
    )
    def _get_final(self, teacher, pk, status):
        return get_object_or_404(Final.objects, teacher=teacher, id=pk, status=status)
