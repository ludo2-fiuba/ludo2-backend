from django.db import models
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    correlatives = models.ManyToManyField("self", blank=True, symmetrical=False)  # TODO check reciprocation

    PASSING_GRADE = 4
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
