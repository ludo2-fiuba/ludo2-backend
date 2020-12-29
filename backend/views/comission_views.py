from rest_framework.permissions import IsAuthenticated

from backend.permissions import IsTeacher
from backend.services.siu_service import SiuService
from backend.views.base_view import BaseViewSet
from backend.views.utils import respond_2


class ComissionViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]

    def list(self, request, *args, **kwargs):
        result = SiuService().list_comissions(request.user.teacher.siu_id)
        return respond_2(result)
