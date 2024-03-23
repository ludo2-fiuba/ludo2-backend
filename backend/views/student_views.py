from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.serializers.student_serializer import StudentSerializer
from backend.views.base_view import BaseViewSet

from ..models import Student


class StudentViews(BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @swagger_auto_schema(
        tags=["Students"],
        operation_summary="Get a student by padron",
        manual_parameters=[
            openapi.Parameter('padron', openapi.IN_QUERY, description="Id of student to get submissions from", type=openapi.FORMAT_INT64)
        ]
    )
    def list(self, request):

        student = get_object_or_404(Student.objects, padron=request.query_params["padron"])

        return Response(self.get_serializer(student, many=False).data, status=status.HTTP_201_CREATED)


