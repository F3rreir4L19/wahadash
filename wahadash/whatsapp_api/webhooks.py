from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import WahaInstance
from chats.models import Chat, Message
from django.utils import timezone
from datetime import datetime

@csrf_exempt
def waha_webhook(request):
    """
    Webhook que recebe todos os eventos do WAHA - VERSÃO CORRIGIDA
    """
    print("🎯" * 10 + " WEBHOOK INICIADO " + "🎯" * 10)
    
    if request.method == 'POST':
        try:
            # Log básico
            print(f"📨 Método: POST | IP: {request.META.get('REMOTE_ADDR')}")
            
            # Ler e parsear dados
            body = request.body.decode('utf-8')
            data = json.loads(body)
            
            event_type = data.get('event')
            instance_name = data.get('instance', 'unknown')
            
            print(f"🔵 Evento: {event_type}")
            print(f"🔵 Instância: {instance_name}")
            
            if event_type == 'message':
                message_data = data.get('data', {})
                print(f"📨 MENSAGEM: {message_data.get('body', '')}")
                print(f"👤 De: {message_data.get('from', '')}")
                
                # Identificar instância CORRETAMENTE
                instance = identify_instance(instance_name)
                if instance:
                    print(f"✅ Instância identificada: {instance.name}")
                    save_message_from_webhook(instance, message_data)
                    print("💾 Mensagem salva com sucesso!")
                else:
                    print("❌ Instância não identificada")
                    # Debug: listar instâncias disponíveis
                    instances = WahaInstance.objects.all()
                    print(f"📋 Instâncias no BD: {[i.name for i in instances]}")
            
            print("✅ Webhook processado com sucesso!")
            return JsonResponse({'status': 'success', 'received': True})
            
        except Exception as e:
            print(f"💥 ERRO NO WEBHOOK: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'method not allowed'}, status=405)

def identify_instance(instance_name):
    """
    Identifica a instância APENAS pelo nome - SIMPLIFICADO
    """
    if not instance_name or instance_name == 'unknown':
        print("🔍 Nome da instância não fornecido")
        return None
    
    try:
        instance = WahaInstance.objects.get(name=instance_name)
        print(f"✅ Instância encontrada: {instance_name}")
        return instance
    except WahaInstance.DoesNotExist:
        print(f"❌ Instância não encontrada: {instance_name}")
        return None

def save_message_from_webhook(instance, message_data):
    """
    Salva mensagem no banco de dados
    """
    try:
        chat_id = message_data.get('chatId')
        content = message_data.get('body', '')
        message_id = message_data.get('id', '')
        from_number = message_data.get('from', '')
        
        # Timestamp
        timestamp = message_data.get('timestamp')
        if timestamp:
            message_time = datetime.fromtimestamp(timestamp)
        else:
            message_time = timezone.now()
        
        print(f"💾 Salvando: {from_number} -> {content}")
        
        # Criar ou buscar chat
        chat, created = Chat.objects.get_or_create(
            chat_id=chat_id,
            waha_instance=instance,
            defaults={'contact_name': from_number}
        )
        
        # Criar mensagem
        Message.objects.create(
            chat=chat,
            message_id=message_id,
            content=content,
            timestamp=message_time,
            direction='in',
            sender=from_number,
            waha_instance=instance
        )
        
        print("✅ Mensagem salva no banco!")
        
    except Exception as e:
        print(f"❌ Erro ao salvar mensagem: {e}")
        raise