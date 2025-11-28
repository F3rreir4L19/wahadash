from django.core.management.base import BaseCommand
from whatsapp_api.models import WahaInstance
from whatsapp_api.waha_manager import waha_manager

class Command(BaseCommand):
    help = 'Inicializa instâncias WAHA no gerenciador'
    
    def handle(self, *args, **options):
        instances = WahaInstance.objects.filter(is_active=True)
        
        for instance in instances:
            waha_manager.add_instance(
                name=instance.name,
                api_url=instance.api_url,
                api_key=instance.api_key
            )
            
        self.stdout.write(
            self.style.SUCCESS(f'{instances.count()} instâncias WAHA inicializadas')
        )