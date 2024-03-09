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
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_datetime, teacher_not_in_commission_staff


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

        submission.grade = grade
        submission.grader = request.user.teacher
        submission.updated_at = get_current_datetime()
        submission.save()
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

        submission.grader = grader_teacher
        submission.updated_at = get_current_datetime()
        submission.save()
        return Response(EvaluationSubmissionSerializer(submission).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        tags=["Evaluation Submissions"],
        operation_summary="Automatically assigns grader teachers to an evaluation"
    )
    def auto_assign_graders(self, request):
        evaluation: Evaluation = get_object_or_404(Evaluation.objects, id=request.data['evaluation'])

        # TODO: check que solo el jefe de catedra puede auto-asignar correctores

        teacher_roles = list(evaluation.semester.commission.teacher_role.all())
        submissions = list(evaluation.submissions.all())

        # B sumarizar cant profs ya asignados y sin asignar
        grader_map = {
            "alvaro": 8,
            "martin": 2,
            "unassigned": 10
        }

        # C calcular total submissions
        total_submissions = submissions.count()

        # D contar ideal segun weights y total
        total_weight = sum(role.grader_weight for role in teacher_roles)
        ideal_graders = {role.teacher_id: 1 for role in teacher_roles} # assign at least one to each in first pass
        ideal_graders = {role.teacher_id: int((role.grader_weight / total_weight) * total_submissions) for role in teacher_roles}
        for role in teacher_roles:
            ideal_graders[role.teacher_id]

        # E mapa con ideal-ya asignados
        current_graders = {role.teacher_id: submissions.filter(grader_id=role.teacher_id).count() for role in teacher_roles}

        # F asignar graders
        for role in teacher_roles:
            ideal_count = ideal_graders.get(role.teacher_id, 0)
            current_count = current_graders.get(role.teacher_id, 0)
            remaining_count = ideal_count - current_count

            if remaining_count > 0:
                unassigned_submissions = submissions.filter(grader_id__isnull=True)
                unassigned_submissions = unassigned_submissions.exclude(grader_id=role.teacher_id)
                unassigned_submissions = unassigned_submissions[:remaining_count]
                
                for submission in unassigned_submissions:
                    submission.grader = role.teacher
                    submission.save()

        return Response(EvaluationSubmissionSerializer(submission).data, status=status.HTTP_200_OK)


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