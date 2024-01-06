from django.db import models
from django.utils import timezone

from .semester import Semester
from .student import Student


class Attendance(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='asistencias', verbose_name="Semestre")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='asistencias', verbose_name="Estudiante")
    submitted_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Fecha de escaneo")
    qr_generated_at = models.DateTimeField(editable=False, null=False, verbose_name="Fecha de generacion del QR escaneado")

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.semester} - {self.student} - {self.submitted_at} - {self.qr_generated_at}"
