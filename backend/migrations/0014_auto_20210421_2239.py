# Generated by Django 3.1.2 on 2021-04-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20210317_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='final',
            name='subject_name',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
