from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whatsapp/', include('whatsapp_api.urls')),  # ← ISSO AQUI!
    path('chats/', include('chats.urls')),
    path('accounts/', include('accounts.urls')),
]