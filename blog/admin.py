from django.contrib import admin
from .models import BlogPost, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'date_created')
    list_filter = ('category', 'status', 'date_created')
    search_fields = ('title', 'content')
