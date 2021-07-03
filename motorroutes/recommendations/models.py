from django.db import models
from django.contrib.auth.models import User
from apps_generic.whodidit.models import WhoDidIt
from accounts.models import UserProfile
from navigation.models import UserLocation,Points,Routes



class UserPoint(WhoDidIt):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    point = models.ForeignKey(Points, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.userprofile)

    # def save(self, *args, **kwargs):
    #     super().save(self, *args, **kwargs)
    #     # TODO: add calculation similarity_score and add record to table Similarity


class UserRoute(WhoDidIt):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.userprofile)


class Similarity(WhoDidIt):
    attraction_point = models.OneToOneField(Points, related_name='attraction_point', on_delete=models.CASCADE,null=True, blank=True)
    user_point = models.OneToOneField(UserPoint, related_name='user_point', on_delete=models.CASCADE,null=True, blank=True)
    similarity_score = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return str(self.similarity_score)
