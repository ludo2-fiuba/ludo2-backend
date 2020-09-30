from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.interactors.final_dates_manager_interactor import FinalDatesManagerInteractor
from backend.interactors.final_interactor import FinalInteractor
from backend.models import Final
from backend.permissions import *
from backend.serializers.final_serializer import FinalTeacherSerializer
from backend.utils import response_error_msg


class FinalTeacherViewSet(viewsets.ModelViewSet):
    queryset = Final.objects.all()
    serializer_class = FinalTeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def detail(self, request, pk=None):
        final = get_object_or_404(Final.objects, id=pk, course__teacher=request.user.teacher)
        return Response(self.serializer_class(final).data)

    @action(detail=True, methods=['POST'])
    def close(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().close(final)
        return self._respond(result, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def send_act(self, _, pk):
        final = get_object_or_404(Final.objects, id=pk)
        result = FinalInteractor().send_act(final)
        return self._respond(result, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'POST'])
    def final_dates(self, request, pk):
        final = get_object_or_404(Final.objects, id=pk)
        if request.method == 'GET':
            result = FinalDatesManagerInteractor(final.course).list()
        else:
            result = FinalDatesManagerInteractor(final.course).set(request['dates'])
        return self._respond(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def set_final_dates(self, request):
        pass

    def _respond(self, result, status):
        if result.errors:
            return Response(response_error_msg(result.errors), status=status)
        else:
            return Response(status=status.HTTP_200_OK)

