from django.db import models
from django.conf import settings

class Chat(models.Model):
    chat_id = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    waha_instance = models.ForeignKey('whatsapp_api.WahaInstance', on_delete=models.CASCADE)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['chat_id', 'waha_instance']
    
    def __str__(self):
        return f"{self.contact_name} ({self.chat_id})"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_id = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField()
    direction = models.CharField(max_length=10, choices=[('in', 'Recebida'), ('out', 'Enviada')])
    sender = models.CharField(max_length=255)
    waha_instance = models.ForeignKey('whatsapp_api.WahaInstance', on_delete=models.CASCADE)
    message_type = models.CharField(max_length=50, default='text')
    
    class Meta:
        ordering = ['timestamp']
        unique_together = ['message_id', 'waha_instance']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"