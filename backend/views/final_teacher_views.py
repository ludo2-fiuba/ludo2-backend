from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from backend.interactors.final_interactor import FinalInteractor
from backend.interactors.siu_interactor import SiuInteractor
from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer
from backend.views.utils import respond


class FinalTeacherViewSet(viewsets.ModelViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def list(self, request):
        result = SiuInteractor().finals(request.user.teacher)
        return respond(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def detail(self, request, pk=None):
        final = get_object_or_404(Final.objects, id=pk)
        result = SiuInteractor().final(final.siu_id, request.user.teacher)
        return respond(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def close(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().close(final)
        return respond(result, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def send_act(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().send_act(final)
        return respond(result, status=status.HTTP_400_BAD_REQUEST)
