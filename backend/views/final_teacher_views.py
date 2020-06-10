from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer, FinalSerializer


class FinalTeacherViewSet(viewsets.ModelViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        final = get_object_or_404(Final.objects, id=pk, teacher=request.user.teacher)
        return Response(FinalTeacherSerializer(final).data)
