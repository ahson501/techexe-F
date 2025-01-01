from django.db import models
from django.contrib.auth.models import AbstractUser
 

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Plant model for catalog and detail pages
class Plant(models.Model):
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    care_instructions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plants', default=1)  
    
    def __str__(self):
        return self.name

# About Us information
class About(models.Model):
    title = models.CharField(max_length=200, default="About Us")
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return self.title

# Contact information
class ContactInfo(models.Model):
    address = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    map_link = models.URLField(blank=True, null=True)  # Link to Google Maps

    def __str__(self):
        return f"Contact Info - {self.email}"

# Testimonials for the home page or about page
class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.name}"

# Featured plants for the home page
class FeaturedPlant(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Featured: {self.plant.name}"


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

