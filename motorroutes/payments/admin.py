from django.contrib import admin

from .models import Transaction, CancelRefundRequests

admin.site.register(Transaction)

admin.site.register(CancelRefundRequests)
