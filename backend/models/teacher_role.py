from django.db import models

from .commission import Commission
from .teacher import Teacher


class TeacherRole(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='teachers', verbose_name="Profesores")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='semesters', verbose_name="Semestres")

    class Role(models.TextChoices):
        TEACHER = 'T', 'Teacher'
        ASSISSTANT = 'A', 'Assisstant'
        COLLABORATOR = 'C', 'Collaborator'

    role = models.CharField(
      max_length=1,
      choices=[(name, name.value) for name in Role],  # Choices is a list of Tuple
      default=Role.TEACHER,
      verbose_name="Rol"
    )

    class Meta:
        verbose_name = "Rol de Profesor"
        verbose_name_plural = "Rol de Profesor"

    def __str__(self):
        return f"{self.commission} - {self.teacher} {self.role}"