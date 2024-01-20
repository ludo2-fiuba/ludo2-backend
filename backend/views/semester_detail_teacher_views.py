from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models.semester import Semester
from backend.permissions import *
from backend.serializers.semester_serializer import SemesterSerializer
from backend.serializers.student_serializer import StudentSerializer
from backend.views.base_view import BaseViewSet


class SemesterDetailTeacherViews(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @action(detail=True, methods=['GET'])
    @swagger_auto_schema(
        tags=["Semesters Teacher"],
        operation_summary="List students enrolled in a particular semester"
    )
    def students(self, request, pk=None):
        semester = get_object_or_404(self.queryset, id=pk)
        teacher = request.user.teacher

        commission = semester.commission
        if teacher not in commission.teachers.all() and commission.chief_teacher != teacher:
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        return Response(StudentSerializer(semester.students, many=True).data, status.HTTP_200_OK)
