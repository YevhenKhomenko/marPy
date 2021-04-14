from django.db import models
from django.contrib.auth.models import User

from apps_generic.whodidit.models import WhoDidIt


class Manufacturer(WhoDidIt):
    name = models.CharField(verbose_name="Name", max_length=200)
    description = models.TextField(verbose_name='Description', max_length=5000)
    
    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return 'Manufacturer {}'.format(self.name)


class Product(WhoDidIt):

    name = models.CharField(verbose_name="Name", max_length=200)
    description = models.TextField(verbose_name='Description', max_length=5000)
    vendor_code = models.IntegerField(verbose_name="Vendor Code")
    #vendor_code_old = models.CharField(verbose_name="Vendor Code OLD", max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name="Name", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return 'Product {}:{} by {}'.format(self.name, self.vendor_code, self.manufacturer)

