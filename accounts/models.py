from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse

# Choices for user type
USER_TYPE_CHOICES = (
    ('community', 'Community Member'),
    ('staff', 'Staff Member'),
)

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='community')
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
    
    def get_verification_token(self):
        """Generate verification token using Django's default token generator"""
        return default_token_generator.make_token(self)
    
    def get_uid(self):
        """Get urlsafe base64 encoded user ID"""
        return urlsafe_base64_encode(force_bytes(self.pk))
    
    def get_absolute_url(self):
        """Get the user profile URL"""
        return reverse('profile', kwargs={'username': self.username})
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

