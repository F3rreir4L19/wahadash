import requests
from django.conf import settings

class WahaManager:
    def __init__(self):
        self.instances = {}
        
    def add_instance(self, name, api_url, api_key):
        self.instances[name] = {
            'api_url': api_url,
            'api_key': api_key,
            'headers': {
                'Content-Type': 'application/json',
                'X-Api-Key': api_key
            }
        }
    
    def send_message(self, instance_name, chat_id, text):
        instance = self.instances.get(instance_name)
        if not instance:
            return {'error': 'Instância não encontrada'}
            
        url = f"{instance['api_url']}/api/sendText"
        data = {
            "chatId": chat_id,
            "text": text,
            "session": "default"
        }
        
        try:
            response = requests.post(
                url, 
                json=data, 
                headers=instance['headers'],
                timeout=30
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'Erro na comunicação: {str(e)}'}
    
    def get_chats(self, instance_name):
        instance = self.instances.get(instance_name)
        if not instance:
            return {'error': 'Instância não encontrada'}
            
        url = f"{instance['api_url']}/api/chats"
        
        try:
            response = requests.get(url, headers=instance['headers'], timeout=30)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'Erro na comunicação: {str(e)}'}

# Singleton
waha_manager = WahaManager()