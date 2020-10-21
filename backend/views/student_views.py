from rest_framework.views import APIView

from backend.serializers.student_serializer import StudentSerializer
from ..models import Student


class StudentViews(APIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
