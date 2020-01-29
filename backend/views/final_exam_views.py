from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from backend.models import FinalExam
from backend.serializers.final_exam_serializer import FinalExamSerializer


class FinalExamViewSet(viewsets.ModelViewSet):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def approved(self, request):
        approved_finals = FinalExam.objects.all().filter(student=request.user.id)

        page = self.paginate_queryset(approved_finals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(approved_finals, many=True)
        return Response(serializer.data)
