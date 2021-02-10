from django.db import models
from .user import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department_siu_id = models.IntegerField(db_index=True, default=0, null=False)

    class Meta:
        verbose_name = "Usuario Administrador"
        verbose_name_plural = "Usuarios Administradores"
