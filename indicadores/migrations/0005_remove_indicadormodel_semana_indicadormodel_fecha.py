# Generated by Django 4.0.3 on 2022-03-24 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0004_indicadormodel_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicadormodel',
            name='semana',
        ),
        migrations.AddField(
            model_name='indicadormodel',
            name='fecha',
            field=models.CharField(default='', max_length=80),
        ),
    ]
