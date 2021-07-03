from django.db import models
from accounts.models import UserProfile


class UserLocation(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    user_lat = models.FloatField(('Latitude'), blank=True, null=True)
    user_lon = models.FloatField(('Longitude'), blank=True, null=True)

    def __str__(self):
        return str(self.userprofile)


class Points(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    ratingvoicecount = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    worktime = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    foundingdate = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    latlongdms = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(('Latitude'), blank=True, null=True)
    longitude = models.FloatField(('Longitude'), blank=True, null=True)
    userlocation = models.ForeignKey(UserLocation, on_delete=models.CASCADE, null=True, blank=True)
    attractions = models.BooleanField(verbose_name='attractions', default=False)

    def __str__(self):
        return self.title


class Routes(models.Model):
    points = models.ManyToManyField(Points)
    distance = models.FloatField(blank=True, null=True)
    shared_with = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.shared_with
