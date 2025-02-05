# Generated by Django 2.2.10 on 2021-07-03 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0012_auto_20210607_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('ratingvoicecount', models.IntegerField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('worktime', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=300, null=True)),
                ('foundingdate', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.CharField(blank=True, max_length=200, null=True)),
                ('latlongdms', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('attractions', models.BooleanField(default=False, verbose_name='attractions')),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_lat', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('user_lon', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(blank=True, null=True)),
                ('points', models.ManyToManyField(to='navigation.Points')),
                ('shared_with', models.ManyToManyField(to='accounts.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='points',
            name='userlocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='navigation.UserLocation'),
        ),
    ]
