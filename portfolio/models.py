from django.db import models
from datetime import datetime
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from PIL import Image

class Portfolio(models.Model):
    TECHNOLOGY_CHOICES = [
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('React', 'React'),
        ('SNMP','SNMP'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='images/')
    url = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=30, choices=TECHNOLOGY_CHOICES)
    date_pub = models.DateTimeField(default=datetime.now, blank=True)
    content = RichTextField(default="Default content here.")


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Optimize uploaded images
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Portfolio Project'
        verbose_name_plural = 'Portfolio Projects'
        ordering = ['-date_pub']
