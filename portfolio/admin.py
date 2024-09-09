from django.contrib import admin
from .models import Portfolio
from .models import ContactInfo
# Register your models here.


admin.site.register(ContactInfo)
admin.site.register(Portfolio)