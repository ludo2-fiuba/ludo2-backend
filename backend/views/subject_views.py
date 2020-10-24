from rest_framework import viewsets, status
from rest_framework.decorators import action

from backend.permissions import *
from backend.interactors.siu_interactor import SiuInteractor
from backend.permissions import IsStudent, IsTeacher
from backend.views.utils import respond


class SubjectViews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsStudent, IsTeacher]

    def list(self, request):
        result = SiuInteractor().subjects()
        respond(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["GET"])
    def correlatives(self, request, pk):
        result = SiuInteractor().correlative_subjects(pk)
        respond(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
