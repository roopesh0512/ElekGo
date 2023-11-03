from rest_framework import serializers
from .models import CustomUser, UserDetails


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
        'id', 'mobile_number', 'is_verified', 'otp', 'is_active', 'is_staff', 'date_joined', 'created_at', 'updated_at')


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'user', 'full_name', 'gender']
