# Generated by Django 2.2.16 on 2021-07-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_auto_20210715_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID категории'),
        ),
    ]