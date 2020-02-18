from django.core.validators import MinLengthValidator
from django.db import models
from .user import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    padron = models.CharField(max_length=6, validators=[MinLengthValidator(5)], blank=True)

    REQUIRED_FIELDS = ['padron']

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name} ({self.padron})"

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
