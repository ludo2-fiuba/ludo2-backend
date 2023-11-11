from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from ..services.siu_service import SiuService
from .final import Final
from .student import Student


class FinalExam(models.Model):
    final = models.ForeignKey(Final, on_delete=models.CASCADE, related_name='final_exams', verbose_name="Final")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='final_exams', verbose_name="Estudiante")
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, db_index=True, verbose_name="Nota")

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Creado en")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Última actualización")

    ALLOWED_FILTERS = {
        "year": "final__date__year",
        "grade_gte": "grade__gte",
        "subject": "final__subject_name__unaccent__icontains",
        "student": "student",
        "status": "final__status"
    }

    PASSING_GRADE = 4

    def date(self):
        return self.final.date

    def subject_name(self):
        return self.final.subject_name

    def subject(self):
        return self.final.subject()

    def teacher(self):
        return self.final.teacher

    def teacher_name(self):
        return f"{self.final.teacher.user.first_name} {self.final.teacher.user.last_name}"

    def act(self):
        return self.final.act

    def correlatives_approved(self):
        siu_subject = SiuService().get_subject(self.final.subject_siu_id)
        correlatives = SiuService().correlative_subjects(siu_subject)
        final_exams = FinalExam.objects.filter(final__subject_siu_id__in=[subject['id'] for subject in correlatives], grade__gte=self.PASSING_GRADE, student=self.student)
        return len(final_exams) == len(correlatives)

    def __str__(self):
        return f"{self.student} - {self.final.date} - {self.grade}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['final', 'student'], name='one_final_exam_per_student')
        ]

        verbose_name = "Exámen final"
        verbose_name_plural = "Exámenes finales"
