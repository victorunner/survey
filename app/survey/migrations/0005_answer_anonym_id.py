# Generated by Django 2.2.16 on 2021-07-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20210708_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='anonym_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
