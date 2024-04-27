from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models.semester import Commission, Semester
from backend.permissions import *
from backend.serializers.semester_serializer import (SemesterPostSerializer,
                                                     SemesterSerializer)
from backend.serializers.student_serializer import StudentSerializer
from backend.views.base_view import BaseViewSet
from backend.views.utils import (datetime_format,
                                 teacher_not_in_commission_staff)


class SemesterDetailTeacherViews(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterPostSerializer
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
        if teacher_not_in_commission_staff(teacher, commission):
            return Response("Teacher not a member of this semester commission", status=status.HTTP_403_FORBIDDEN)

        return Response(StudentSerializer(semester.students, many=True).data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Semesters"],
        operation_summary="Create a semester"
    )
    def create(self, request):
        commission = get_object_or_404(Commission, id=request.data['commission'])
        
        if request.data['year_moment'] not in Semester.YearMoment.values:
            return Response("Invalid year moment", status=status.HTTP_400_BAD_REQUEST)
        
        start_date = datetime_format(request.data['start_date'])
        if not start_date:
            return Response("Invalid start date", status=status.HTTP_400_BAD_REQUEST)

        if commission.chief_teacher != request.user.teacher:
            return Response("Teacher not chief teacher in commission", status=status.HTTP_403_FORBIDDEN)

        semesters_in_commission = Semester.objects.filter(commission=commission).all()

        already_exists = False
        for semester in semesters_in_commission:
            if (semester.start_date.year == start_date.year and
                request.data['year_moment'] == semester.year_moment):
                already_exists = True

        if already_exists:
            return Response("Semester already exists", status=status.HTTP_403_FORBIDDEN)
        
        classes_amount = request.data['classes_amount']
        minimum_attendance = request.data['minimum_attendance']

        if not classes_amount:
            classes_amount = 16

        if not minimum_attendance:
            minimum_attendance = 0.0
            
        semester = Semester(
            commission=commission,
            year_moment=request.data['year_moment'],
            start_date=start_date,
            classes_amount=classes_amount,
            minimum_attendance=minimum_attendance
        )

        semester.save()
        
        return Response(SemesterSerializer(semester, many=False).data, status.HTTP_200_OK)
