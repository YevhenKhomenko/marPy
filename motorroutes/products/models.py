from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from apps_generic.whodidit.models import WhoDidIt


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)
        
        
class SoftDeletionManager(models.Manager):
    #def __init__(self, *args, **kwargs):
    #    self.alive_only = kwargs.pop('alive_only', True)
    #    super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(is_deleted=False)

        
class Manufacturer(WhoDidIt):
    name = models.CharField(verbose_name="Name", max_length=200)
    description = models.TextField(verbose_name='Description', max_length=5000)
    
    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return 'Manufacturer {}'.format(self.name)


class Product(WhoDidIt):
    is_deleted = models.BooleanField(verbose_name='Is deleted', default=False)
    deleted_on = models.DateTimeField(verbose_name='deleted_on', blank=True, null=True)
    deleted_by = models.ForeignKey(User, verbose_name='deleted by', on_delete=models.SET_NULL, blank=True, null=True)
    
    name = models.CharField(verbose_name="Name", max_length=200)
    description = models.TextField(verbose_name='Description', max_length=5000)
    vendor_code = models.IntegerField(verbose_name="Vendor Code", null=True, blank=True)
    #vendor_code_old = models.CharField(verbose_name="Vendor Code OLD", max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name="Name", on_delete=models.SET_NULL, null=True, blank=True)
    objects = SoftDeletionManager()
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return 'Product {}:{} by {}'.format(self.name, self.vendor_code, self.manufacturer)
        
        
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_on = timezone.now()
        self.save()
