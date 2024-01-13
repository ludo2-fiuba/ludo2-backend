import uuid
from django.db import models
from django.utils import timezone

from .semester import Semester
from .teacher import Teacher


class AttendanceQRCode(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='attendance_qrs', verbose_name="Semestre")
    owner_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendances_qrs', verbose_name="Docente que creo el QR")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Fecha de creacion")
    qrid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "QR de Asistencias"
        verbose_name_plural = "QRs de Asistencias"

    def __str__(self):
        return f"{self.semester} - {self.owner_teacher} - {self.created_at} - {self.qrid}"
