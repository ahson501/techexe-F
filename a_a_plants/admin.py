from django.contrib import admin
from .models import Plant

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available', 'price', 'url')  # Columns in admin list view
    list_filter = ('category', 'available')  # Filter options in admin
    search_fields = ('name', 'category')  # Searchable fields
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from name
