from django.contrib import admin
from .models import CustomUser, UserDetails
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserDetails)