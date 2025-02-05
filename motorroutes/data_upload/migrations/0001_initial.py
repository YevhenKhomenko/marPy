# Generated by Django 2.2.10 on 2021-06-28 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendataionsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='when created')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='when updated')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_upload_recommendataionsdata_created_by', to=settings.AUTH_USER_MODEL, verbose_name='who created')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_upload_recommendataionsdata_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='when updated')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
