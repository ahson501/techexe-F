from django.contrib import admin
from .models import Course, Chapter, Videos

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('title', 'description')
    ordering = ('-date_created',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'date_created')
    list_filter = ('course', 'date_created')
    search_fields = ('title',)
    ordering = ('course', 'order')

class VideosAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'chapter', 'date_created')
    list_filter = ('course', 'chapter', 'date_created')
    search_fields = ('title', 'description')
    ordering = ('-date_created',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Videos, VideosAdmin)
