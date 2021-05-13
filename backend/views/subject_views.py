from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import IsStudent
from backend.serializers.final_exam_serializer import FinalExamSerializer
from backend.services.siu_service import SiuService
from backend.views.utils import respond_plain


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = FinalExamSerializer
    queryset = FinalExam.objects.all()

    @action(detail=False, methods=["GET"])
    def history(self, request):
        result = self.get_queryset().filter(final__subject_siu_id=request.query_params['subject_siu_id'], student=request.user.id).order_by('final__date')
        return Response(FinalExamSerializer(result, many=True).data, status.HTTP_200_OK)

    def list(self, request):
        result = SiuService().list_subjects()
        return respond_plain(result)
