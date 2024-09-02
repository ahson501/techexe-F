from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'technologies', 'demo_link', 'image')
    search_fields = ('title', 'description', 'technologies')
