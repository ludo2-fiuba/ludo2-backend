from django.db import models
from django.utils import timezone

from . import Final, Student
from django.core.validators import MinValueValidator, MaxValueValidator


class FinalExam(models.Model):
    final = models.ForeignKey(Final, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['final', 'student'], name='one_final_exam_per_student')
        ]
