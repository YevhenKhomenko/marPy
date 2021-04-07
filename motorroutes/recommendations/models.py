from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Place(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    user_ratings = models.FloatField(null=True, blank=True)
    num_rated = models.IntegerField(null=True, blank=True)
    comparable = models.BooleanField(default=True)
    liked = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.title


class Similarity(models.Model):
    first_place = models.ForeignKey(Place, related_name='first_place', on_delete=models.CASCADE)
    second_place = models.ForeignKey(Place, related_name='second_place', on_delete=models.CASCADE)
    similarity_score = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return self.similarity_score


class OnlineLink(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user_id = models.IntegerField(null=True, blank=True)
    gallery_id = models.IntegerField(null=True, blank=True)
    blog_id = models.IntegerField(null=True, blank=True)
    google_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user_id
