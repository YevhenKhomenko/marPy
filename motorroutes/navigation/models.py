from django.db import models
from django.contrib.auth.models import User


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lat = models.FloatField(('Latitude'), blank=True, null=True)
    lon = models.FloatField(('Longitude'), blank=True, null=True)

    def __str__(self):
        return f"user:{str(self.user)},lat:{str(self.lat)},lon{str(self.lon)}"


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
        return f"id:{str(self.id)},title:{str(self.title)},attractions:{str(self.attractions)},lat:{str(self.latitude)},lon{str(self.longitude)}"


class Routes(models.Model):
    points = models.ManyToManyField(Points)
    distance = models.FloatField(blank=True, null=True)
    shared_with = models.ManyToManyField(User)

    def __str__(self):
        return f"id:{str(self.id)},points:{str(self.points)},distance:{str(self.distance)}"
