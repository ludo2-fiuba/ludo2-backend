from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from backend.interactors.final_interactor import FinalInteractor
from backend.interactors.siu_interactor import SiuInteractor
from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer
from backend.views.utils import respond


class FinalTeacherViewSet(viewsets.ModelViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request):
        result = SiuInteractor().finals(request.user.teacher, request.query_params['subject_siu_id'])
        return respond(result)

    def create(self, request):
        pass

    def detail(self, request, pk=None):
        final = get_object_or_404(Final.objects, teacher=request.user.teacher, id=pk)
        return respond(self.get_serializer(final))

    @action(detail=True, methods=['POST'])
    def close(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().close(final)
        return respond(result)

    @action(detail=True, methods=['POST'])
    def send_act(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().send_act(final)
        return respond(result)
