# Generated by Django 3.2 on 2021-05-05 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210409_1217'),
        ('recommendations', '0006_auto_20210505_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='userprofile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
    ]