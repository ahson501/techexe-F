from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture', 'designation', 'country', 'city')
    search_fields = ('user__username', 'user__email', 'bio', 'designation', 'country', 'city')
