from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from .models import WahaInstance, InstanceSession
from .waha_manager import waha_manager
from accounts.permissions import user_has_instance_access
from django.utils import timezone
import json

@method_decorator(login_required, name='dispatch')
class InstanceListView(ListView):
    model = WahaInstance
    template_name = 'whatsapp_api/instance_list.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return WahaInstance.objects.all()
        return self.request.user.userprofile.allowed_instances.all()

@method_decorator(login_required, name='dispatch')
class SwitchInstanceView(View):
    def post(self, request, instance_id):
        # Verificar se usuário tem acesso à instância
        if not user_has_instance_access(request.user, instance_id):
            return JsonResponse({'status': 'error', 'message': 'Acesso negado'}, status=403)
            
        instance = get_object_or_404(WahaInstance, id=instance_id)
        
        # Ativar sessão para esta instância
        InstanceSession.objects.filter(user=request.user).update(is_active=False)
        session, created = InstanceSession.objects.get_or_create(
            user=request.user,
            instance=instance,
            defaults={'is_active': True}
        )
        session.is_active = True
        session.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Instância alterada para {instance.name}',
            'instance': {
                'name': instance.name,
                'number': instance.whatsapp_number
            }
        })

@method_decorator(login_required, name='dispatch')
class SendMessageView(View):
    def post(self, request, instance_id):
        # Verificar se usuário tem acesso à instância
        if not user_has_instance_access(request.user, instance_id):
            return JsonResponse({'status': 'error', 'message': 'Acesso negado'}, status=403)
            
        instance = get_object_or_404(WahaInstance, id=instance_id)
        
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            message = data.get('message')
        except:
            chat_id = request.POST.get('chat_id')
            message = request.POST.get('message')
        
        if not chat_id or not message:
            return JsonResponse({'error': 'chat_id e message são obrigatórios'}, status=400)
        
        result = waha_manager.send_message(
            instance.name,
            chat_id,
            message
        )
        
        if 'error' not in result:
            # Salvar mensagem no histórico
            from chats.models import Chat, Message
            chat, created = Chat.objects.get_or_create(
                chat_id=chat_id,
                waha_instance=instance,
                defaults={'contact_name': chat_id}
            )
            
            Message.objects.create(
                chat=chat,
                message_id=result.get('id', ''),
                content=message,
                timestamp=timezone.now(),
                direction='out',
                sender=instance.whatsapp_number,
                waha_instance=instance
            )
        
        return JsonResponse(result)

@method_decorator(login_required, name='dispatch')
class GetChatsView(View):
    def get(self, request, instance_id):
        # Verificar se usuário tem acesso à instância
        if not user_has_instance_access(request.user, instance_id):
            return JsonResponse({'status': 'error', 'message': 'Acesso negado'}, status=403)
            
        instance = get_object_or_404(WahaInstance, id=instance_id)
        
        result = waha_manager.get_chats(instance.name)
        
        if 'error' in result:
            return JsonResponse(result, status=400)
        
        # Formatar os chats para a resposta
        chats = []
        for chat in result:
            chats.append({
                'id': chat.get('id'),
                'name': chat.get('name'),
                'unread_count': chat.get('unreadCount', 0)
            })
        
        return JsonResponse(chats, safe=False)

@method_decorator(login_required, name='dispatch')
class ChatInterfaceView(View):
    def get(self, request):
        if request.user.is_superuser:
            instances = WahaInstance.objects.all()
        else:
            instances = request.user.userprofile.allowed_instances.all()
        
        return render(request, 'chats/chat_interface.html', {
            'instances': instances
        })