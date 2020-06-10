from django.db import models
from django.utils import timezone

from backend.models import Teacher


class Course(models.Model):
    subject = models.TextField(editable=False, null=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    semester = models.TextField(editable=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    ALLOWED_FILTERS = {
    }

    def __str__(self):
        return f"{self.subject} - {self.semester} - {self.teacher}"

