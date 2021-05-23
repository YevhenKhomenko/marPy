from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps_generic.whodidit.models import WhoDidIt

class Statistic(WhoDidIt):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    count = models.PositiveIntegerField(default=1)

    year = models.IntegerField(db_index=True, null=True, blank=True)
    month = models.IntegerField(db_index=True, null=True, blank=True)
    week = models.IntegerField(db_index=True, null=True, blank=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'year', 'month', 'week')