# Generated by Django 3.1.2 on 2024-02-03 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_attendance_attendanceqrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='parent_evaluation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='make_up_evaluation', to='backend.evaluation', verbose_name='Evaluacion a recuperar'),
        ),
    ]
