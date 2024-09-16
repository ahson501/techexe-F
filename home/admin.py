from django.contrib import admin
from .models import HomeContent

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'description', 'image')
    search_fields = ('title', 'subtitle', 'description')
