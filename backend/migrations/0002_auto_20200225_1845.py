# Generated by Django 3.0.2 on 2020-02-25 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='correlatives',
            field=models.ManyToManyField(blank=True, related_name='_subject_correlatives_+', to='backend.Subject'),
        ),
    ]
