import uuid

from django.db import models
from django.utils import timezone

from backend.models import Commission
from backend.services.siu_service import SiuService
from backend.utils import memoized


class Semester(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='semesters', verbose_name="Semestres")

    class YearMoment(models.TextChoices):
        FIRST_SEMESTER = 'FS', 'First Semester'
        SECOND_SEMESTER = 'SS', 'Second Semester'
        INTENSIVE_WINTER = 'IW', 'Intensive Winter'
        INTENSIVE_SUMMER = 'IS', 'Intensive Summer'
    
    year_moment = models.CharField(
      max_length=2,
      choices=[(moment, moment.value) for moment in YearMoment],  # Choices is a list of Tuple
      default=YearMoment.FIRST_SEMESTER,
      verbose_name="Momento del año"
    )
    start_date = models.DateTimeField(db_index=True, verbose_name="Fecha de inicio")

    # REQUIRED_FIELDS = ['date']

    # ALLOWED_FILTERS = {
    #     "year": "date__year",
    #     "grade_gte": "finalexam__grade__gte",
    #     "student": "finalexam__student"
    # }

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"

    def __str__(self):
        return f"{self.commission} - {self.start_date} {self.year_moment}"
