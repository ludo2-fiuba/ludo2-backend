from django.db import models

from .semester import Semester


class Evaluation(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='evaluations', verbose_name="Evaluaciones")
    evaluation_name = models.CharField(max_length=100, db_index=True, editable=False, verbose_name="Nombre de Evaluacion")
    is_graded = models.BooleanField(default=True)
    passing_grade = models.IntegerField(db_index=True, blank=True,verbose_name="Nota de Aprobacion")


    start_date = models.DateTimeField(db_index=True, blank=True, verbose_name="Fecha de inicio")
    end_date = models.DateTimeField(db_index=True, verbose_name="Fecha de entrega")


    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluation"

    def __str__(self):
        return f"{self.semester} - {self.evaluation_name}"