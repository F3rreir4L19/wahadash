from django.contrib import admin
from .models import WahaInstance, InstanceSession

@admin.register(WahaInstance)
class WahaInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'api_url', 'whatsapp_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'whatsapp_number']

@admin.register(InstanceSession)
class InstanceSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'instance', 'is_active', 'last_used']
    list_filter = ['is_active', 'instance', 'last_used']