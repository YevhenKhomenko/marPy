# Generated by Django 3.2 on 2021-05-26 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0004_alter_statistic_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
