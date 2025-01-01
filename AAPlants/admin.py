from django.contrib import admin
from .models import Plant, About, ContactInfo, Testimonial, FeaturedPlant , Category
from django.contrib.auth.models import User
from .models import CustomUser

admin.site.register(Plant)
admin.site.register(About)
admin.site.register(ContactInfo)
admin.site.register(Testimonial)
admin.site.register(FeaturedPlant)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(CustomUser)
