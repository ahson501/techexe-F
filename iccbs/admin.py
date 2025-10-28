from django.contrib import admin
from .models import Profile, NetworkDevice, NetworkInterface, SNMPTrap, SessionAlert, SystemAlert

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture', 'designation', 'country', 'city')
    search_fields = ('user__username', 'user__email', 'bio', 'designation', 'country', 'city')
admin.site.register(NetworkDevice)
admin.site.register(NetworkInterface)
admin.site.register(SNMPTrap)
admin.site.register(SessionAlert)
admin.site.register(SystemAlert)