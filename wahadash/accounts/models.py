from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    # Adicione related_name único para resolver os conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # ← NOME ÚNICO AQUI
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # ← NOME ÚNICO AQUI
        related_query_name="customuser",
    )
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    allowed_instances = models.ManyToManyField('whatsapp_api.WahaInstance', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class AdminAccess(models.Model):
    admin_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_access')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_access')
    waha_instance = models.ForeignKey('whatsapp_api.WahaInstance', on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.admin_user} → {self.user} ({self.waha_instance})"