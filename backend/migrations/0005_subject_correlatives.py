# Generated by Django 3.0.2 on 2020-02-07 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200128_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='correlatives',
            field=models.ManyToManyField(related_name='_subject_correlatives_+', to='backend.Subject'),
        ),
    ]
