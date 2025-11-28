from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Message, Chat
from whatsapp_api.models import WahaInstance
from accounts.permissions import user_has_instance_access

class ChatHistoryView(LoginRequiredMixin, View):
    def get(self, request, instance_id, chat_id):
        # Verificar se usuário tem acesso à instância
        if not user_has_instance_access(request.user, instance_id):
            return JsonResponse({'error': 'Acesso negado'}, status=403)
        
        instance = get_object_or_404(WahaInstance, id=instance_id)
        chat = get_object_or_404(Chat, chat_id=chat_id, waha_instance=instance)
        
        # Buscar mensagens do chat
        messages = Message.objects.filter(chat=chat).order_by('timestamp')
        
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'direction': message.direction,
                'sender': message.sender,
            })
        
        return JsonResponse(messages_data, safe=False)