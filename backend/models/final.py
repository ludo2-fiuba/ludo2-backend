import uuid

from django.db import models
from django.utils import timezone

from .course import Course


class Final(models.Model):

    class Status(models.TextChoices):
        OPEN = 'OP', 'Open'
        PENDING_ACT = 'PA', 'Pending Act'
        ACT_SENT = 'AS', 'Act Sent'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='finals')
    date = models.DateTimeField(db_index=True, null=False, editable=False)
    qrid = models.UUIDField(default=uuid.uuid4, editable=False)
    year_in_school = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['date']

    ALLOWED_FILTERS = {
        "year": "date__year",
        "grade_gte": "finalexam__grade__gte",
        "student": "finalexam__student"
    }

    def subject(self):
        return self.course.subject

    def teacher(self):
        return self.course.teacher

    def __str__(self):
        return f"{self.subject()} - {self.teacher()} - {self.date.date()}"
