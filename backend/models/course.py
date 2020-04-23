from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from backend.models import Subject, Student, Teacher


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses')
    year = models.IntegerField()
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    ALLOWED_FILTERS = {
    }

    def __str__(self):
        return f"{self.subject} - {self.semester}c{self.year} - {self.teacher}"

