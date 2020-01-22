from rest_framework import viewsets

from backend.models import FinalExam
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
