from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.interactors.siu_interactor import SiuInteractor
from backend.views.utils import respond


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        result = SiuInteractor().list_subjects()
        return respond(result)

    @action(detail=True, methods=["GET"])
    def correlatives(self, request, pk):
        result = SiuInteractor().correlative_subjects(pk)
        return respond(result)
