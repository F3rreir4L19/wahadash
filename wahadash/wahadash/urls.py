from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # ← ADICIONE ESTA LINHA

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whatsapp/', include('whatsapp_api.urls')),
    path('chats/', include('chats.urls')),
    path('accounts/', include('accounts.urls')),
    
    # ← ADICIONE ESTAS LINHAS:
    path('', RedirectView.as_view(url='/whatsapp/chat-interface/')),  # Redireciona raiz para o WhatsApp
]