from django.http import HttpResponse
from rest_framework import viewsets

from .models import Student
from .serializers import StudentSerializer


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the backend index.")
