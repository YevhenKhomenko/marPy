from django.contrib import admin

from .models import Similarity, UserPoint, UserRoute

admin.site.register(UserPoint)

admin.site.register(Similarity)

admin.site.register(UserRoute)
