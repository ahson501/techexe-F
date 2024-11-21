from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Plant(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "A&A Plant"
        verbose_name_plural = "A&A Plants"
