from rest_framework.decorators import action
from rest_framework.views import APIView

from ..models import Student
from backend.serializers.student_serializer import StudentSerializer


class StudentViews(APIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['POST'])
    def me(self, request, pk):
        pass
