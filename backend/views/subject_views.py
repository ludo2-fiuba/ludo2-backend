from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.services.siu_service import SiuService
from backend.views.utils import respond_plain


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        result = SiuService().list_subjects()
        return respond_plain(result)
