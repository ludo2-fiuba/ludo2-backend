# Generated by Django 3.1.2 on 2021-04-28 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20210422_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='final',
            name='subject_name',
            field=models.CharField(db_index=True, default='Física I', editable=False, max_length=100, verbose_name='Nombre de Materia'),
            preserve_default=False,
        ),
    ]
