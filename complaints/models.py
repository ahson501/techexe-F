from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class CustomUserComplaints(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)  # Example field

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_complaints_groups',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_complaints_permissions',  # Unique related_name
        blank=True
    )

    def __str__(self):
        return self.username