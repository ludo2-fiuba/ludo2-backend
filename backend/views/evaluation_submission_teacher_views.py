from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import Evaluation, EvaluationSubmission, Semester
from backend.models.teacher import Teacher
from backend.models.teacher_role import TeacherRole
from backend.permissions import *
from backend.serializers.evaluation_submission_serializer import (
    EvaluationSubmissionCorrectionSerializer,
    EvaluationSubmissionPutSerializer, EvaluationSubmissionSerializer)
from backend.services.evaluation_submission_service import EvaluationSubmissionService
from backend.services.grader_assignment_service import GraderAssignmentService
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_datetime, get_stub_chief_teacher_role, teacher_not_in_commission_staff


class EvaluationSubmissionTeacherViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = EvaluationSubmission.objects.all()
    serializer_class = EvaluationSubmissionPutSerializer
        
    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Gets submissions for an evaluation",
        manual_parameters=[
            openapi.Parameter('evaluation', openapi.IN_QUERY, description="Id of evaluation to get submissions from", type=openapi.FORMAT_INT64)
        ]
    )
    def get_submissions(self, request):

        evaluation = get_object_or_404(Evaluation.objects, id=request.query_params["evaluation"])

        commission = evaluation.semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        result = self.queryset.filter(evaluation=request.query_params['evaluation']).all()
        return Response(EvaluationSubmissionCorrectionSerializer(result, many=True).data, status.HTTP_200_OK)
    
    @action(detail=False, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Grades an evaluation submission"
    )
    def grade(self, request):
        grade = request.data['grade']
        submission = self.queryset.filter(student__user__id=request.data['student'], evaluation__id=request.data['evaluation']).first()

        if not submission:
            return Response("Submission not found", status=status.HTTP_404_NOT_FOUND)
        
        commission = submission.evaluation.semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        submissions_service = EvaluationSubmissionService()
        submissions_service.set_grade(submission, request.user.teacher, grade)

        return Response(EvaluationSubmissionSerializer(submission).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Assigns a grader to an evaluation submission"
    )
    def assign_grader(self, request):
        grader_teacher = get_object_or_404(Teacher.objects, user_id=request.data['grader_teacher'])

        submission = self.queryset.filter(student__user__id=request.data['student'], evaluation__id=request.data['evaluation']).first()

        if not submission:
            return Response("Submission not found", status=status.HTTP_404_NOT_FOUND)
        
        if submission.grade:
            return Response("Submission already graded", status=status.HTTP_403_FORBIDDEN)

        commission = submission.evaluation.semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        if teacher_not_in_commission_staff(grader_teacher, commission):
            return Response("Teacher not present in commission's staff", status=status.HTTP_403_FORBIDDEN)

        submissions_service = EvaluationSubmissionService()
        submissions_service.set_grader(submission, request.user.teacher)

        return Response(EvaluationSubmissionSerializer(submission).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['PUT'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Automatically assigns grader teachers to an evaluation"
    )
    def auto_assign_graders(self, request):
        evaluation: Evaluation = get_object_or_404(Evaluation.objects, id=request.data['evaluation'])

        if teacher_not_in_commission_staff(request.user.teacher, evaluation.semester.commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        submissions = list(evaluation.submissions.all())
        teacher_roles = list(evaluation.semester.commission.teacher_roles.all())
        teacher_roles.append(get_stub_chief_teacher_role(evaluation.semester.commission))

        grader_assignment_service = GraderAssignmentService()
        new_submissions = grader_assignment_service.auto_assign(teacher_roles, submissions)

        return Response(EvaluationSubmissionSerializer(new_submissions, many=True).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Gets submissions for an evaluation",
        manual_parameters=[
            openapi.Parameter('student', openapi.IN_QUERY, description="Id of student to get submissions from", type=openapi.FORMAT_INT64),
            openapi.Parameter('semester', openapi.IN_QUERY, description="Id of semester to get submissions from", type=openapi.FORMAT_INT64)
        ]
    )
    def get_submissions_from_student(self, request):

        semester = get_object_or_404(Semester.objects, id=request.query_params["semester"])

        commission = semester.commission
        if teacher_not_in_commission_staff(request.user.teacher, commission):
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        result = self.queryset.filter(evaluation__semester=semester).filter(student__user__id=request.query_params["student"]).all()
        return Response(EvaluationSubmissionCorrectionSerializer(result, many=True).data, status.HTTP_200_OK)