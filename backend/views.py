from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from .serializers import StudentSerializer
from .models import Student
from rest_framework.response import Response

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the backend index.")