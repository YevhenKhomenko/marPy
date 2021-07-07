from django.db import models
from django.contrib.auth.models import User
from apps_generic.whodidit.models import WhoDidIt
from accounts.models import UserProfile
from navigation.models import UserLocation,Points,Routes



class UserPoint(WhoDidIt):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    point = models.ForeignKey(Points, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"user:{str(self.user)},point:{str(self.point)}"


class UserRoute(WhoDidIt):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"user:{str(self.user)},route:{str(self.route)}"


class Similarity(WhoDidIt):
    attraction_point = models.OneToOneField(Points, related_name='attraction_point', on_delete=models.CASCADE,null=True, blank=True)
    user_point = models.OneToOneField(UserPoint, related_name='user_point', on_delete=models.CASCADE,null=True, blank=True)
    similarity_score = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return f"attraction:{str(self.attraction_point)},user:{str(self.user_point)},"
