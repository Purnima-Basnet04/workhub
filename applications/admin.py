from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'status')
    search_fields = ('applicant__username', 'job__title')
    list_filter = ('status',)
    
admin.site.register(Application, ApplicationAdmin)
