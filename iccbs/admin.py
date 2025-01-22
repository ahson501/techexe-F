from django.contrib import admin
from .models import CustomUsericcbs

@admin.register(CustomUsericcbs)
class CustomUsericcbsAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')