from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from .user import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    siu_id = models.IntegerField(db_index=True, default=0, null=False, editable=False)
    legajo = models.CharField(max_length=8, validators=[MinLengthValidator(5)], blank=True)
    face_encodings = ArrayField(base_field=models.FloatField(null=False), blank=False, default=list)

    REQUIRED_FIELDS = ['siu_id', 'legajo']

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name} ({self.legajo})"

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
