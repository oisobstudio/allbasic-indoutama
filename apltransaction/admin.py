from django.contrib import admin
from .models import InvoiceCategory, InvoiceStatus


admin.site.register(InvoiceCategory)
admin.site.register(InvoiceStatus)
