from django.contrib import admin
from .models import Plant, About, ContactInfo, Testimonial, FeaturedPlant

admin.site.register(Plant)
admin.site.register(About)
admin.site.register(ContactInfo)
admin.site.register(Testimonial)
admin.site.register(FeaturedPlant)

