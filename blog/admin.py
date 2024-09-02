from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'image')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('published_date',)
    date_hierarchy = 'published_date'
