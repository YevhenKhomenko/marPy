from django.contrib import admin

from .models import Similarity, Place, OnlineLink

admin.site.register(Place)

admin.site.register(Similarity)

admin.site.register(OnlineLink)
