# Generated by Django 3.1.2 on 2023-12-02 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_auto_20231202_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='teachers',
            field=models.ManyToManyField(through='backend.TeacherRole', to='backend.Teacher', verbose_name='Cuerpo Docente'),
        ),
        migrations.AlterField(
            model_name='teacherrole',
            name='commission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.commission', verbose_name='Profesores'),
        ),
        migrations.AlterField(
            model_name='teacherrole',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.teacher', verbose_name='Semestres'),
        ),
    ]
