from django.db import models

class WahaInstance(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()  # http://localhost:3001, http://localhost:3002
    api_key = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.whatsapp_number})"

class InstanceSession(models.Model):
    instance = models.ForeignKey(WahaInstance, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)