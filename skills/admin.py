from django.contrib import admin

from .models import *

class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    
admin.site.register(Skill, SkillAdmin)
