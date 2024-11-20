from django.contrib import admin
from .models import Portfolio

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'technology', 'date_pub')
    search_fields = ('title', 'description')
