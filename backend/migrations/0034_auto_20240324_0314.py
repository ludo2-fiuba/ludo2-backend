# Generated by Django 3.1.2 on 2024-03-24 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_auditlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='related_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Relacionado'),
        ),
    ]
