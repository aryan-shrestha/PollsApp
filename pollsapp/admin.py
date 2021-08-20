from django.contrib import admin

from pollsapp.models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
