# Generated by Django 3.1.2 on 2021-02-10 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20210201_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='subject_siu_id',
            new_name='department_siu_id',
        ),
    ]
