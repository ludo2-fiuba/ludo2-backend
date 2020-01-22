from rest_framework.views import APIView

from ..models import Student
from ..serializers import StudentSerializer


class StudentsView(APIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
