from django.db import models
from django.utils import timezone

from .evaluation import Evaluation
from .student import Student
from .teacher import Teacher


class EvaluationSubmission(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='submissions', verbose_name="Evaluacion")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions', verbose_name="Estudiante")
    grade = models.IntegerField(null=True, db_index=True, verbose_name="Nota")
    corrector = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, related_name='corrector', verbose_name="Corrector")

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Creado en")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Última actualización")


    def __str__(self):
        return f"{self.student} - {self.evaluation} - {self.grade}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['evaluation', 'student'], name='one_submission_per_student')
        ]

        verbose_name = "Entrega de Evaluacion"
        verbose_name_plural = "Entregas de Evaluacion"
