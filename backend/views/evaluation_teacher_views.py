from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation, Semester
from backend.serializers.evaluation_serializer import EvaluationPostSerializer
from backend.views.base_view import BaseViewSet


class EvaluationTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationPostSerializer
    
    @action(detail=False, methods=['POST'])
    def add_evaluation(self, request):
        evaluation_data = request.data
        evaluation_serializer = EvaluationPostSerializer(data=evaluation_data)
        if evaluation_serializer.is_valid():
            semester = self._semester(evaluation_serializer.initial_data["semester_id"])
            if (semester.commission.chief_teacher == request.user.teacher):
                evaluation_serializer.save()
                return Response(evaluation_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _semester(self, semester_pk):
        return get_object_or_404(Semester.objects, id=semester_pk)
