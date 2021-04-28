# Generated by Django 2.2 on 2021-04-21 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_remove_product_vendor_code_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='deleted by'),
        ),
        migrations.AddField(
            model_name='product',
            name='deleted_on',
            field=models.DateTimeField(blank=True, null=True, verbose_name='deleted_on'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Is deleted'),
        ),
    ]