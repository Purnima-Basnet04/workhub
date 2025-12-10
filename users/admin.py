from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    
    
# Register your models here.
admin.site.register(Profile, ProfileAdmin)
