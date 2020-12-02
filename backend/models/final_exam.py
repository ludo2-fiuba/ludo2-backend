from django.db import models
from django.utils import timezone

from . import Final, Student
from django.core.validators import MinValueValidator, MaxValueValidator


class FinalExam(models.Model):
    final = models.ForeignKey(Final, on_delete=models.CASCADE, related_name='final_exams')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='final_exams')
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, db_index=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    ALLOWED_FILTERS = {
        "year": "final__date__year",
        "grade_gte": "grade__gte",
        "subject": "final__subject_name__contains",
        "student": "student"
    }

    PASSING_GRADE = 4

    def date(self):
        return self.final.date

    def subject(self):
        return self.final.subject_name

    def teacher(self):
        return self.final.teacher

    def __str__(self):
        return f"{self.student} - {self.final.date} - {self.grade}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['final', 'student'], name='one_final_exam_per_student')
        ]
