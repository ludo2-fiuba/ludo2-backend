from django.db import models
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    correlatives = models.ManyToManyField("self", blank=True, symmetrical=False)

    ALLOWED_FILTERS = {
        "name": "name",
        "year": "final__date__year",
        "grade_gte": "final__finalexam__grade__gte",
        "student": "final__finalexam__student"
    }

    PASSING_GRADE = 4
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

