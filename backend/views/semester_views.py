from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import AttendanceQRCode, EvaluationSubmission, Semester
from backend.serializers.attendance_serializer import \
    AttendanceQRCodeStudentsSerializerNoSemester
from backend.serializers.evaluation_submission_serializer import \
    EvaluationSubmissionSerializer
from backend.serializers.semester_serializer import (
    SemesterSerializer, SemesterWithMakeupSerializer)
from backend.serializers.student_serializer import StudentSerializer
from backend.services.rule_engine_service import RuleEngineService
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_semester, get_current_year


class SemesterViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Semesters"],
        operation_summary="Get semesters for a subject",
        manual_parameters=[
            openapi.Parameter('subject_siu_id', openapi.IN_QUERY, description="Id of subject to get semester from", type=openapi.FORMAT_INT64)
        ]
    )
    def subject_semesters(self, request):
        result = self.get_queryset().filter(commission__subject_siu_id=request.query_params['subject_siu_id'])
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Semesters"],
        operation_summary="Get present semester for a subject",
        manual_parameters=[
            openapi.Parameter('subject_siu_id', openapi.IN_QUERY, description="Id of subject to get semester from", type=openapi.FORMAT_INT64)
        ]
    )
    def present_subject_semesters(self, request):
        result = self.get_queryset().filter(commission__subject_siu_id=request.query_params['subject_siu_id'], 
                                            start_date__year__gte=get_current_year(), year_moment=get_current_semester())
        return Response(self.get_serializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Semesters"],
        operation_summary="Get semesters for a commission",
        manual_parameters=[
            openapi.Parameter('commission_id', openapi.IN_QUERY, description="Id of commission to get semester from", type=openapi.FORMAT_INT64)
        ]
    )
    def commission_present_semester(self, request):
        result = self.get_queryset().filter(commission=request.query_params['commission_id'], 
                                            start_date__year__gte=get_current_year(), year_moment=get_current_semester()).first()
        
        if not result:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        return Response(self.get_serializer(result).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    @swagger_auto_schema(
        tags=["Semesters"],
        operation_summary="Return if the student is passing the semester",
        manual_parameters=[
            openapi.Parameter('semester_id', openapi.IN_QUERY, description="Id of semester", type=openapi.FORMAT_INT64)
        ]
    )
    def is_passing(self, request):
        semester = self.get_queryset().filter(id=request.query_params['semester_id']).first()

        attendance_qrs = AttendanceQRCode.objects.all().filter(semester=semester).all()
        evaluation_submissions = EvaluationSubmission.objects.all().filter(evaluation__semester=semester, student=request.user.student).all()
        
        rule_engine_service = RuleEngineService()
        rule_engine_service.generate_passed_rules(SemesterWithMakeupSerializer(semester).data)


        passed = rule_engine_service.is_student_passed(AttendanceQRCodeStudentsSerializerNoSemester(attendance_qrs, many=True).data, 
                                               EvaluationSubmissionSerializer(evaluation_submissions, many=True).data,
                                               StudentSerializer(request.user.student).data, SemesterWithMakeupSerializer(semester).data)
        
        rule_engine_service = RuleEngineService()
        rule_engine_service.generate_failed_rules(SemesterWithMakeupSerializer(semester).data)

        failed = rule_engine_service.is_student_failed(AttendanceQRCodeStudentsSerializerNoSemester(attendance_qrs, many=True).data, 
                                               EvaluationSubmissionSerializer(evaluation_submissions, many=True).data,
                                               StudentSerializer(request.user.student).data)
        
        response = {'passed': passed, 'failed': failed}

        return Response(response, status.HTTP_200_OK)

