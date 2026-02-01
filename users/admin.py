from django.contrib import admin
from .models import *
from skills.models import Skill

class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 1
class EducationInline(admin.StackedInline):
    model = Education
    extra = 1
class CertificationInline(admin.StackedInline):
    model = Certification
    extra = 1   
class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    extra = 1
class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    inlines = [ExperienceInline, EducationInline, CertificationInline, SocialLinkInline, ProjectInline]  
    
admin.site.register(Profile, ProfileAdmin)
