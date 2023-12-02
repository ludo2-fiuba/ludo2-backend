# Generated by Django 3.1.2 on 2023-12-02 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_evaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('T', 'T'), ('A', 'A'), ('C', 'C')], default='T', max_length=1, verbose_name='Rol')),
                ('commission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='backend.commission', verbose_name='Profesores')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='backend.teacher', verbose_name='Semestres')),
            ],
            options={
                'verbose_name': 'Rol de Profesor',
                'verbose_name_plural': 'Rol de Profesor',
            },
        ),
    ]
