from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from backend.interactors.siu_interactor import SiuInteractor
from backend.permissions import IsTeacher
from backend.views.utils import respond


class ComissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request, *args, **kwargs):
        result = SiuInteractor().list_comissions(request.user.teacher.pk) # TODO: change for siu_id
        return respond(result, status.HTTP_200_OK)
