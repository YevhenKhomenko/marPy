from django.db import models
from accounts.models import UserProfile


class Location(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.userprofile)


class Points(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=100)
    gallery_id = models.IntegerField(blank=True, null=True)
    blog_id = models.IntegerField(blank=True, null=True)
    google_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Routes(models.Model):
    first_point = models.OneToOneField(Points, related_name='first_point', on_delete=models.CASCADE)
    second_point = models.OneToOneField(Points, related_name='second_point', on_delete=models.CASCADE)
    distance = models.FloatField(blank=True, null=True)
    shared_with = models.ManyToManyField(UserProfile, related_name="shared_with")

    def __str__(self):
        return str(self.shared_with)
