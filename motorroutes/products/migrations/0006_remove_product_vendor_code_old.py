# Generated by Django 2.2 on 2021-04-14 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210414_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vendor_code_old',
        ),
    ]