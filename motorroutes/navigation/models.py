from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	lat = models.FloatField(('Latitude'), blank=True, null=True)
	lon = models.FloatField(('Longitude'),blank=True, null=True)
	
	def __str__(self):
		return self.user_id
		
		
class Points(models.Model):
	name = models.CharField(max_length=200)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	description = models.CharField(max_length=500)
	address = models.CharField(max_length=100)
	gallery_id = models.IntegerField(blank=True, null=True)
	blog_id = models.IntegerField(blank=True, null=True)
	google_id = models.CharField(max_length=500)
	
	def __str__(self):
		return self.name


class Routes(models.Model):
	points = models.ManyToManyField(Points)
	distance = models.FloatField(blank=True, null=True)
	shared_with = models.ManyToManyField(User)
	
	def __str__(self):
		return self.shared_with
	
	

 
