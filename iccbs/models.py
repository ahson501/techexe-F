from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Picture and Basic Info
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    link1 = models.URLField(blank=True, null=True, verbose_name="Computational Experiments-01")
    link2 = models.URLField(blank=True, null=True, verbose_name="Computational Experiments-02")
    link3 = models.URLField(blank=True, null=True, verbose_name="Computational Experiments-03")

    # Add the designation field
    designation = models.CharField(max_length=100, blank=True, null=True)

    # Academic and Professional Details
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=150, blank=True, null=True)

    # Research and Contributions
    research_interests = models.TextField(blank=True, null=True)
    publications = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    

    # Professional Skills and Certifications
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    # Networking and Links
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    google_scholar = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    portfolio = models.URLField(max_length=200, blank=True, null=True)

    # Field-Specific Information
    expertise = models.TextField(blank=True, null=True)
    tools = models.TextField(blank=True, null=True)

    # Collaboration and Availability
    mentorship_offered = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Demographics
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # Customizable Fields
    tagline = models.CharField(max_length=150, blank=True, null=True)
    quote = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

      

# Automatically create or update the Profile when a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
