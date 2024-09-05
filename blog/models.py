from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from taggit.managers import TaggableManager

class Course(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    tags = TaggableManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos-detail', kwargs={'pk': self.pk})

class Videos(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    title = models.CharField(max_length=150)
    video = models.FileField(upload_to='videos', null=True, validators=[
        FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])
    ])
    thumbnail = models.ImageField(upload_to='thumbnails')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos-detail', kwargs={'pk': self.pk})


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

