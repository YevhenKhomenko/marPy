from django.db import models
from apps_generic.whodidit.models import WhoDidIt
import jsonfield
from django.utils import timezone

class Statistic(WhoDidIt):
    object_id = models.PositiveIntegerField(db_index=True)
    count = models.PositiveIntegerField(default=1)
    date =  models.DateField(default=timezone.now)
    action = jsonfield.JSONField(default=list)

    class Meta:
        unique_together = ('date', 'object_id')