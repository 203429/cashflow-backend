# Generated by Django 4.0.3 on 2022-03-23 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flujos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flujomodel',
            name='fecha',
            field=models.CharField(max_length=80),
        ),
    ]
