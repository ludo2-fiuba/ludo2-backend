from datetime import datetime

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from backend.interactors.final_interactor import FinalInteractor
from backend.interactors.siu_interactor import SiuInteractor
from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond


class FinalTeacherViewSet(BaseViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request):
        result = SiuInteractor().get_subject(request.query_params['subject_siu_id'])
        finals = self.queryset.filter(teacher=request.user.teacher, subject=result.data['name'])
        return self._paginate(finals)

    def create(self, request):
        result = SiuInteractor().create_final(request.user.teacher, request.data['subject_siu_id'], request.data["timestamp"])
        final = Final(
            siu_id=result.data["id"],
            subject=request.data['subject_name'],
            date=datetime.utcfromtimestamp(request.data['timestamp']),
            teacher=request.user.teacher)
        final.save()
        return respond(self.get_serializer(final))

    def detail(self, request, pk=None):
        return respond(self.get_serializer(self._get_final(request.user.teacher, pk)))

    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        result = FinalInteractor().close(self._get_final(request.user.teacher, pk))
        return respond(self.get_serializer(result.data))

    @action(detail=True, methods=['POST'])
    def send_act(self, request, pk):
        result = FinalInteractor().send_act(self._get_final(request.user.teacher, pk))
        return respond(self.get_serializer(result.data))

    def _get_final(self, teacher, pk):
        return get_object_or_404(Final.objects, teacher=teacher, id=pk)
