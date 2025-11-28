import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class WahaManager:
    def __init__(self):
        self.instances = {}
        print("🔄 WAHA Manager inicializado")
        
    def add_instance(self, name, api_url, api_key):
        self.instances[name] = {
            'api_url': api_url,
            'api_key': api_key,
            'headers': {
                'Content-Type': 'application/json',
                'X-Api-Key': api_key
            }
        }
        print(f"✅ Instância adicionada: {name} -> {api_url}")
    
    def get_chats(self, instance_name):
        print(f"🔍 Buscando chats para instância: {instance_name}")
        
        instance = self.instances.get(instance_name)
        if not instance:
            error_msg = f"Instância não encontrada: {instance_name}. Instâncias disponíveis: {list(self.instances.keys())}"
            print(f"❌ {error_msg}")
            return {'error': error_msg}
            
        url = f"{instance['api_url']}/api/chats"
        print(f"📡 URL da API: {url}")
        
        try:
            response = requests.get(url, headers=instance['headers'], timeout=30)
            print(f"📡 Status Code: {response.status_code}")
            print(f"📡 Resposta: {response.text}")
            
            if response.status_code == 200:
                chats = response.json()
                print(f"✅ Chats recebidos: {len(chats)}")
                return chats
            else:
                error_msg = f"Erro {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {'error': error_msg}
                
        except requests.exceptions.RequestException as e:
            error_msg = f'Erro na comunicação com WAHA: {str(e)}'
            print(f"❌ {error_msg}")
            return {'error': error_msg}

# Singleton
waha_manager = WahaManager()