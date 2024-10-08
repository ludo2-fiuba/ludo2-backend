# Generated by Django 3.1.2 on 2020-10-26 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='final',
            name='status',
            field=models.CharField(choices=[('OP', 'OP'), ('PA', 'PA'), ('AS', 'AS')], default='OP', max_length=2),
        ),
        migrations.AlterField(
            model_name='final',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='finals', to='backend.teacher'),
        ),
    ]
