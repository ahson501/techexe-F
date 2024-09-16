from django.db import models
from datetime import datetime
from django.utils.text import slugify

class Portfolio(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Add this line
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=30)
    date_pub = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Meta:
    verbose_name = 'Portfolio Project'
    verbose_name_plural = 'Portfolio Projects'
    ordering = ['-date_pub']


class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email
