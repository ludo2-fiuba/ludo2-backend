from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from backend.services.siu_service import SiuService
from backend.permissions import IsTeacher
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond


class ComissionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request, *args, **kwargs):
        result = SiuService().list_comissions(request.user.teacher.pk) # TODO: change for siu_id
        return respond(result, status.HTTP_200_OK)
