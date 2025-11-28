from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, AdminAccess

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_staff', 'is_active']
    list_filter = ['is_admin', 'is_staff', 'is_active']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    filter_horizontal = ['allowed_instances']

@admin.register(AdminAccess)
class AdminAccessAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'user', 'waha_instance', 'granted_at', 'is_active']
    list_filter = ['is_active', 'waha_instance']