from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Picture and Basic Info
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = RichTextField(blank=True, null=True, default='')
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

    # Contact Me Details
    contact_email = models.EmailField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

      

# Automatically create or update the Profile when a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# ===================== NETWORK MONITORING MODELS =====================

class NetworkDevice(models.Model):
    """Stores SNMP-capable devices"""
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    snmp_version = models.CharField(max_length=10, default='v3')
    context = models.CharField(max_length=100, blank=True, null=True)
    auth_protocol = models.CharField(max_length=20, default='SHA')
    priv_protocol = models.CharField(max_length=20, default='AES')
    auth_password = models.CharField(max_length=100, blank=True, null=True)
    priv_password = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class NetworkInterface(models.Model):
    """Represents each interface on a network device"""
    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, related_name='interfaces')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    if_index = models.IntegerField()
    speed = models.BigIntegerField(blank=True, null=True)
    admin_status = models.BooleanField(default=True)
    oper_status = models.BooleanField(default=True)
    last_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device.name} - {self.name}"


class SNMPTrap(models.Model):
    """Stores SNMP Traps received from devices"""
    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, related_name='traps')
    trap_oid = models.CharField(max_length=200)
    trap_type = models.CharField(max_length=100, blank=True, null=True)  # linkUp, linkDown, coldStart, etc.
    message = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=[
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ], default='info')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trap_type} on {self.device.name} at {self.timestamp}"


class SessionAlert(models.Model):
    """Tracks ISP or user session alerts"""
    isp_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('up', 'Up'),
        ('down', 'Down'),
        ('flapping', 'Flapping'),
    ], default='up')
    reason = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.isp_name} - {self.status}"


class SystemAlert(models.Model):
    """System-level alerts (CPU, Memory, Disk, etc.)"""
    hostname = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=100)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ], default='info')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname}: {self.alert_type} ({self.severity})"