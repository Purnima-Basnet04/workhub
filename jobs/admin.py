from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "recruiter", "location", "employment_type", "work_mode", "created_at")
    search_fields = ("title", "company", "location", "recruiter__username")
    list_filter = ("employment_type", "work_mode", "created_at")
    ordering = ("-created_at",)
    
admin.site.register(Job, JobAdmin)


