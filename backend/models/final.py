import uuid

from django.db import models
from django.utils import timezone


class Final(models.Model):

    class Status(models.TextChoices):
        OPEN = 'OP', 'Open'
        PENDING_ACT = 'PA', 'Pending Act'
        ACT_SENT = 'AS', 'Act Sent'

    date = models.DateTimeField(db_index=True, null=False, editable=False)
    qrid = models.UUIDField(default=uuid.uuid4, editable=False)
    siu_id = models.IntegerField(db_index=True, default=0, null=False, editable=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['date']

    ALLOWED_FILTERS = {
        "year": "date__year",
        "grade_gte": "finalexam__grade__gte",
        "student": "finalexam__student"
    }

    def __str__(self):
        return f"{self.id} - {self.siu_id} - {self.date.date()}"
