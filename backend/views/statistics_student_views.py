from datetime import timedelta

from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import FinalExam
from backend.permissions import *
from backend.views.base_view import BaseViewSet
from backend.views.utils import get_current_datetime


class StatisticstudentViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsStudent]


    @swagger_auto_schema(
        tags=["Statistics"],
        operation_summary="Gets your average grade compared to the average of every student"
    )
    def list(self, request):
        results = {}

        # Average Over Time

        average_over_time = []
        student_final_exams = FinalExam.objects.filter(student=request.user.student).filter(grade__gte=4).values('final__date').annotate(grade=Avg('grade')).all()
        if student_final_exams:
            average_over_time = self._average_over_time(student_final_exams)

        results['average_over_time'] = average_over_time


        # Student Average vs Global Average
        
        student_average = FinalExam.objects.filter(student=request.user.student).filter(grade__gte=4).aggregate(student_average=Avg('grade'))
        global_average = FinalExam.objects.filter(grade__gte=4).values('student').annotate(average_grade=Avg('grade')).aggregate(global_average=Avg('average_grade'))
        
        results['student_vs_global_average'] = {**student_average, **global_average}

        # Best Subjects

        student_subject_name_average = FinalExam.objects.filter(student=request.user.student).filter(grade__gte=4).values('final__subject_name').annotate(average_grade=Avg('grade')).all()
        subject_name_average = FinalExam.objects.filter(grade__gte=4).values('final__subject_name').annotate(average_grade=Avg('grade')).all()
        student_subject_average_dict = {result['final__subject_name']: result['average_grade'] for result in student_subject_name_average}
        subject_average_dict = {result['final__subject_name']: result['average_grade'] for result in subject_name_average}

        best_subjects = []
        worst_of_best = None

        for subject in student_subject_average_dict:
            average_diff = student_subject_average_dict[subject] - subject_average_dict[subject]
            
            if (worst_of_best is None) or ((worst_of_best['grade'] - worst_of_best['subject_average']) < average_diff) or (len(best_subjects) < 3):
                if(len(best_subjects) == 3):
                    best_subjects.remove(worst_of_best)
                best_subjects.append({'subject': subject, 'grade': student_subject_average_dict[subject], 'subject_average': subject_average_dict[subject]})

                worst = None

                for best_subject in best_subjects:
                    if (worst is None) or ((worst['grade'] - worst['subject_average']) > (best_subject['grade'] - best_subject['subject_average'])) or (
                            (worst['grade'] - worst['subject_average']) == (best_subject['grade'] - best_subject['subject_average']) and worst['grade'] > best_subject['grade']):
                        worst = best_subject
                worst_of_best = worst

        sorted_best_subjects = sorted(best_subjects, key=lambda x: (x['grade'] - x['subject_average'], x['grade']), reverse=True)

        results['best_subjects'] = sorted_best_subjects

        
        return Response(results, status.HTTP_200_OK)
    

    def _average_over_time(self, student_final_exams):
        average_over_time = []

        min_date = min(student_final_exams, key=lambda x: x['final__date'])['final__date']
        days_difference = (get_current_datetime() - min_date).days
        
        for i in range(6):
            days_sum = (days_difference / 6) * (i + 1)
            max_date = min_date + timedelta(days=days_sum)
            exams_for_interval = [entry for entry in student_final_exams if entry['final__date'] <= max_date]
            grades = [entry['grade'] for entry in exams_for_interval]
            average = sum(grades) / len(grades)
            year_month = f'{max_date.month}/{str(max_date.year)[-2:]}'
            average_over_time.append({'date': year_month, 'average': average})

        return average_over_time