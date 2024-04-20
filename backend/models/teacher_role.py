from django.db import models

from .commission import Commission
from .teacher import Teacher


class TeacherRole(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, verbose_name="Profesores", related_name='teacher_roles')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Semestres")
    grader_weight = models.FloatField(default=1.0, verbose_name="Peso al asignar correctores")
    role = models.CharField(max_length=25, null=False, verbose_name="Rol")

    class Meta:
        verbose_name = "Rol de Profesor"
        verbose_name_plural = "Rol de Profesor"

    def __str__(self):
        return f"{self.teacher} - {self.role} - {self.grader_weight}"
