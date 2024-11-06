from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return self.title