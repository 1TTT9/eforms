from django.contrib import admin

# Register your models here.

from .models import EFMRequest06, EFMRequest03

admin.site.register(EFMRequest06)
admin.site.register(EFMRequest03)
