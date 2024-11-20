from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Define the STATUS choices
STATUS = (
    (0, "Draft"),
    (1, "Publish"),
)

# Define the Category model with predefined choices
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('React', 'React'),
        ('SNMP', 'SNMP'),
        ('Botany', 'Botany'),
    ]

    name = models.CharField(max_length=100, unique=True, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Added SlugField

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Define the BlogPost model with a ForeignKey to Category
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(choices=STATUS, default=0)  # Adding status field with Draft as default
    url = models.URLField(max_length=200, blank=True, null=True)  # Added URL field (optional)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.slug})
