from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'chat_id', 'waha_instance', 'is_group', 'created_at']
    list_filter = ['waha_instance', 'is_group', 'created_at']
    search_fields = ['contact_name', 'chat_id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'content_preview', 'direction', 'waha_instance', 'timestamp']
    list_filter = ['direction', 'waha_instance', 'timestamp']
    search_fields = ['sender', 'content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'