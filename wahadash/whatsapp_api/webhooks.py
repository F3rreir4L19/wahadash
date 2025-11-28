from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import WahaInstance
from chats.models import Chat, Message
from django.utils import timezone

@csrf_exempt
def waha_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_type = data.get('event')
            
            if event_type == 'message':
                message_data = data.get('data', {})
                
                # Identificar instância pelo IP ou cabeçalho personalizado
                instance = identify_instance(request)
                if instance:
                    save_message_from_webhook(instance, message_data)
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            print(f"Erro no webhook: {e}")
            return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'method not allowed'}, status=405)

def identify_instance(request):
    # Lógica para identificar qual instância WAHA enviou o webhook
    client_ip = request.META.get('REMOTE_ADDR')
    # Mapear IP para instância (configurável via admin)
    try:
        return WahaInstance.objects.get(server_ip=client_ip)
    except WahaInstance.DoesNotExist:
        return None

def save_message_from_webhook(instance, message_data):
    chat_id = message_data.get('chatId')
    content = message_data.get('body', '')
    message_id = message_data.get('id', '')
    timestamp = message_data.get('timestamp', timezone.now())
    from_number = message_data.get('from', '')
    
    chat, created = Chat.objects.get_or_create(
        chat_id=chat_id,
        waha_instance=instance,
        defaults={'contact_name': from_number}
    )
    
    Message.objects.create(
        chat=chat,
        message_id=message_id,
        content=content,
        timestamp=timestamp,
        direction='in',
        sender=from_number,
        waha_instance=instance
    )