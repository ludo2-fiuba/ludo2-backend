from django.db import models
from django.utils import timezone

from .user import User


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs', verbose_name="Usuario")
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Usuario Relacionado")
    log = models.TextField(verbose_name="Texto de evento")
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Fecha de evento")

    class Meta:
        verbose_name = "Registro de Auditoria"
        verbose_name_plural = "Registro de Auditoria"

    def __str__(self):
        return f"{self.user} - {self.log}"