from django.db import models
from apps_generic.whodidit.models import WhoDidIt
import json
from navigation.models import UserLocation, Points, Routes
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
            if not v['skip_item']:
                created_point = Points.objects.get_or_create(
                    title=v.get('titletext'),
                    description=v.get('description'),
                    rating=v.get('rating'),
                    ratingvoicecount=v.get('ratingvoicecount'),
                    phone=v.get('phone'),
                    worktime=v.get('worktime'),
                    category=v.get('category'),
                    foundingdate=v.get('foundingdate'),
                    email=v.get('email'),
                    website=v.get('website'),
                    latlongdms=v.get('latlongdms'),
                    latitude=v.get('Latitude'),
                    longitude=v.get('Longitude'),
                    attractions=True, )
