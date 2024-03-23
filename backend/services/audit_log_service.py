from django.db import IntegrityError, transaction

from backend.models import AuditLog


class AuditLogService:

    def log(self, user, related_user, text):

        print(text)
        AuditLog(user=user, related_user=related_user, log=text).save()
