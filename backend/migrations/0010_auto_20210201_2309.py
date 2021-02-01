# Generated by Django 3.1.2 on 2021-02-01 23:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20210122_2306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='final',
            options={'verbose_name': 'Final', 'verbose_name_plural': 'Finales'},
        ),
        migrations.AlterModelOptions(
            name='finalexam',
            options={'verbose_name': 'Exámen final', 'verbose_name_plural': 'Exámenes finales'},
        ),
        migrations.AlterModelOptions(
            name='finaltoapprove',
            options={'verbose_name': 'Fecha para aprobar', 'verbose_name_plural': 'Fechas para aprobar'},
        ),
        migrations.AlterModelOptions(
            name='preregisteredstudent',
            options={'verbose_name': 'Estudiante pre registrado', 'verbose_name_plural': 'Estudiantes pre registrados'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': 'Usuario Administrador', 'verbose_name_plural': 'Usuarios Administradores'},
        ),
        migrations.AlterModelOptions(
            name='staffuser',
            options={'verbose_name': 'Usuario Administrador', 'verbose_name_plural': 'Usuarios Administradores'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Estudiante', 'verbose_name_plural': 'Estudiantes'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Docentes', 'verbose_name_plural': 'Docentes'},
        ),
        migrations.AlterField(
            model_name='final',
            name='act',
            field=models.CharField(db_index=True, max_length=10, null=True, verbose_name='Nro de Acta'),
        ),
        migrations.AlterField(
            model_name='final',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Creado en'),
        ),
        migrations.AlterField(
            model_name='final',
            name='date',
            field=models.DateTimeField(db_index=True, editable=False, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='final',
            name='status',
            field=models.CharField(choices=[('DF', 'DF'), ('RJ', 'RJ'), ('OP', 'OP'), ('PA', 'PA'), ('AS', 'AS')], default='DF', max_length=2, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='final',
            name='subject_name',
            field=models.CharField(db_index=True, editable=False, max_length=100, verbose_name='Nombre de Materia'),
        ),
        migrations.AlterField(
            model_name='final',
            name='subject_siu_id',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='SIU ID de Materia'),
        ),
        migrations.AlterField(
            model_name='final',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='finals', to='backend.teacher', verbose_name='Docente'),
        ),
        migrations.AlterField(
            model_name='final',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Última Actualización'),
        ),
    ]
