from django.db import models

class HomeContent(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='home_images/', blank=True, null=True)

    def __str__(self):
        return self.title
