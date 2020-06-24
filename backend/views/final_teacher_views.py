from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer


class FinalTeacherViewSet(viewsets.ModelViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def detail(self, request, pk=None):
        final = get_object_or_404(Final.objects, id=pk, course__teacher=request.user.teacher)
        return Response(self.serializer_class(final).data)
