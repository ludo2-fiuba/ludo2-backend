from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correlatives = models.ManyToManyField("self", blank=True, symmetrical=False)  # TODO check reciprocation

    PASSING_GRADE = 4
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
