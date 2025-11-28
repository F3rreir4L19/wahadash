from django.core.exceptions import PermissionDenied

def user_has_instance_access(user, instance_id):
    if user.is_superuser:
        return True
        
    try:
        from whatsapp_api.models import WahaInstance
        instance = WahaInstance.objects.get(id=instance_id)
        return user.userprofile.allowed_instances.filter(id=instance_id).exists()
    except:
        return False

class InstanceAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        instance_id = kwargs.get('instance_id')
        if not user_has_instance_access(request.user, instance_id):
            raise PermissionDenied("Você não tem acesso a esta instância")
        return super().dispatch(request, *args, **kwargs)