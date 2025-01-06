from django.contrib import admin
from .models import Plant, About, ContactInfo, Testimonial, FeaturedPlant, Category, CustomUserAAPlants

admin.site.register(About)
admin.site.register(ContactInfo)
admin.site.register(Testimonial)
admin.site.register(FeaturedPlant)
admin.site.register(Category)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

@admin.register(CustomUserAAPlants)
class CustomUserAAPlantsAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  
    search_fields = ('username', 'email')
