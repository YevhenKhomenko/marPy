# Generated by Django 3.2 on 2021-04-28 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210409_1217'),
        ('recommendations', '0004_alter_place_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinelink',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
            preserve_default=False,
        ),
    ]
