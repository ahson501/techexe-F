
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUsericcbs(AbstractUser):
    """Custom user model extending AbstractUser."""
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Example additional field

    def __str__(self):
        return self.username

# Profile Model
class Profile(models.Model):
    """Extended profile for users."""
    user = models.OneToOneField(CustomUsericcbs, on_delete=models.CASCADE)  # Link to Custom User model
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
