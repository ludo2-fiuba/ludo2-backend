from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from rest_framework import status

from backend.interactors.course_refresher_interactor import CourseRefresherInteractor
from backend.models.course import Course
from backend.permissions import *
from backend.serializers.course_serialiazer import CourseSerializer


class CourseTeacherViewSet(viewsets.ModelViewSet):
    queryset = Course.objects
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def list(self, request):
        courses = self.queryset.filter(teacher=request.user.teacher)
        return Response(self.serializer_class(courses, many=True).data)

    def detail(self, request, pk=None):
        course = get_object_or_404(self.queryset, id=pk, teacher=request.user.teacher)
        return Response(self.serializer_class(course).data)

    @action(detail=False, methods=['GET'])
    def refresh(self, request):
        result = CourseRefresherInteractor(request.user.teacher).refresh()
        if result.is_successful():
            return Response(data=result.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=result.data, status=status.HTTP_200_OK)
