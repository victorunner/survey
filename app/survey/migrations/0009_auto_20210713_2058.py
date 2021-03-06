# Generated by Django 2.2.16 on 2021-07-13 20:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20210713_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choices',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='answer to open-ended question'),
        ),
    ]
