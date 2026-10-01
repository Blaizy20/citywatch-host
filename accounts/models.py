from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('admin', 'Admin/LGU Staff'),
        ('personnel', 'Field Personnel'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    phone_number = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    sex = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def is_personnel(self):
        return self.role == 'personnel'

    def is_resident(self):
        return self.role == 'resident'


class OTPChallenge(models.Model):
    PURPOSE_CHOICES = [
        ('registration', 'Registration'),
        ('password_reset', 'Password reset'),
    ]

    email = models.EmailField(db_index=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    code_hash = models.CharField(max_length=256)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.purpose} OTP for {self.email}"