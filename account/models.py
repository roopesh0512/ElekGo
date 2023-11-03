from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .choices import COUNTRY, GENDER

from account.managers import CustomUserManager


# TeioxRoopeshPassword


class CustomUser(AbstractBaseUser, PermissionsMixin):
    country = models.CharField(choices=COUNTRY, max_length=50, help_text="Please Select Country", default="INDIA (+91)")
    mobile_number = models.CharField(unique=True, max_length=15)
    email = models.EmailField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'

    def __str__(self):
        return self.mobile_number


class UserDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_details")
    full_name = models.CharField(max_length=30, null=False, blank=False, help_text="Full Name")
    gender = models.CharField(choices=GENDER, max_length=15, help_text="Gender")

    def __str__(self):
        return self.full_name
