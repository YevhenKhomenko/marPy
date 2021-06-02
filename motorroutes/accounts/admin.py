from django.contrib import admin
from .models import UserProfile, UserAuthCredentials

admin.site.register(UserProfile)
admin.site.register(UserAuthCredentials)
