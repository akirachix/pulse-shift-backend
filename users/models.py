from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=20, unique=True)
    image_url = models.URLField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class MamaMboga(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mama_mboga')
    kiosk_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    image_url = models.URLField(null=True, blank=True)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    address_description = models.TextField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.kiosk_name


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    is_default = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Address {self.address_id} for {self.customer} ({self.latitude}, {self.longitude})"


class AdminModeratorProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_mod_profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


User = get_user_model()


class DashboardAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_admin_profile')  # Fixed related_name here
    is_active = models.BooleanField(default=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
