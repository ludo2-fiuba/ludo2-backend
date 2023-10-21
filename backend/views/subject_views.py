from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.api_exceptions import InvalidSubjectCodeError
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

    @action(detail=False, methods=["GET"])
    def correlatives(self, request):
        self.extra = {}
        id = request.query_params.get('id')
        response = SiuService().list_subjects({'id': id})

        if not response:
            raise InvalidSubjectCodeError()

        result = SiuService().correlative_subjects(response[0])
        return respond_plain(result)

    def list(self, request):
        result = SiuService().list_subjects()
        return respond_plain(result)
