from django.contrib import admin

from .models import Product, History, Purchase

# Register your models here.

admin.site.register(Product)
admin.site.register(History)
admin.site.register(Purchase)
