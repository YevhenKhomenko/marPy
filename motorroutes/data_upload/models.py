from django.db import models
from apps_generic.whodidit.models import WhoDidIt
from django.utils import timezone
import json
from navigation.models import UserLocation, Points, Routes
import datetime
from accounts.models import UserProfile
from django.contrib.auth.models import User


class RecommendationsData(WhoDidIt):
    name = models.CharField(verbose_name="Name", max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(self, *args, **kwargs)
        with open(self.file.path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            if not data[k]['skip_item']:
                created_point = Points.objects.get_or_create(
                    title=data[k]['titletext'],
                    description=data[k]['description'],
                    rating=data[k]['rating'],
                    ratingvoicecount=data[k]['ratingvoicecount'],
                    phone=data[k]['phone'],
                    worktime=data[k]['worktime'],
                    category=data[k]['category'],
                    foundingdate=data[k]['foundingdate'],
                    email=data[k]['email'],
                    website=data[k]['website'],
                    latlongdms=data[k]['latlongdms'],
                    latitude=data[k]['Latitude'],
                    longitude=data[k]['Longitude'],
                    attractions = True,)
