from django.db import models

from .semester import Semester
from .student import Student


class CommissionInscription(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Semester")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")

    class InscriptionStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        CANCELLED = 'C', 'Cancelled'
        REJECTED = 'R', 'Rejected'

    status = models.CharField(
        max_length=1,
        choices=[(status, status.value) for status in InscriptionStatus],  # Choices is a list of Tuple
        default=InscriptionStatus.PENDING,
        verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Inscripcion a Cursada"
        verbose_name_plural = "Inscripciones a Cursadas"

    def __str__(self):
        return f"{str(self.student)} - {str(self.semester)}"