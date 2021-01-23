from django.db import models
from .user import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject_siu_id = models.IntegerField(db_index=True, default=0, null=False)
