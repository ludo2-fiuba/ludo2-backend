from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.interactors.final_dates_manager_interactor import FinalDatesManagerInteractor
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

    @action(detail=True, methods=['GET', 'POST'])
    def final_dates(self, request, pk):
        final = get_object_or_404(Final.objects, id=pk)
        if request.method == 'GET':
            result = FinalDatesManagerInteractor(final.course).list()
        else:
            result = FinalDatesManagerInteractor(final.course).set(request['dates'])
        if result.errors:
            return Response(result.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def set_final_dates(self, request):
        pass
