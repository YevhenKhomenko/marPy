from django.db import models
from apps_generic.whodidit.models import WhoDidIt
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

class Statistic(WhoDidIt):
    object_id = models.PositiveIntegerField(db_index=True)
    count = models.PositiveIntegerField(default=1)
    date =  models.DateTimeField(default=timezone.now)
    action = JSONField(default=list)