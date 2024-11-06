from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','date_created')
    list_filter = ('date_created',)  # Add a comma to make it a tuple
    search_fields = ('title', 'content')
    date_hierarchy = 'date_created'
    list_per_page = 20

admin.site.register(BlogPost, BlogPostAdmin)
