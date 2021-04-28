from django.db import models
from django.contrib.auth.models import User
from apps_generic.whodidit.models import WhoDidIt
from accounts.models import UserProfile

# Create your models here.
class Place(WhoDidIt):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    user_ratings = models.FloatField(null=True, blank=True)
    num_rated = models.IntegerField(null=True, blank=True)
    comparable = models.BooleanField(default=True)
    liked = models.BooleanField(null=True, blank=True)
    #TODO add ForeignKey to Navigation

    def __str__(self):
        return str(self.title)


class Similarity(WhoDidIt):
    first_place = models.OneToOneField(Place, related_name='first_place', on_delete=models.CASCADE)
    second_place = models.OneToOneField(Place, related_name='second_place', on_delete=models.CASCADE)
    similarity_score = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return str(self.similarity_score)


class OnlineLink(WhoDidIt):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    gallery_id = models.IntegerField(null=True, blank=True)
    blog_id = models.IntegerField(null=True, blank=True)
    google_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user_id)
