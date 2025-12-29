from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'public_url', 'created_by', 'created_at')
    search_fields = ('name', 'public_url', 'created_by__username')
    prepopulated_fields = {'public_url': ('name',)}

admin.site.register(Company, CompanyAdmin)