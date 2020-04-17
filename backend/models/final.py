from django.utils import timezone

from .subject import Subject
from .teacher import Teacher
from django.db import models


class Final(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['date']

    ALLOWED_FILTERS = {
        "year": "date__year",
        "grade_gte": "finalexam__grade__gte",
        "student": "finalexam__student"
    }
