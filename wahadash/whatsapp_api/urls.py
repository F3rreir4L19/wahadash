from django.urls import path
from . import webhooks
from . import views

urlpatterns = [
    path('webhook/', webhooks.waha_webhook, name='waha_webhook'),
    path('switch-instance/<int:instance_id>/', views.SwitchInstanceView.as_view(), name='switch_instance'),
    path('send/<int:instance_id>/', views.SendMessageView.as_view(), name='send_message'),
    path('chats/<int:instance_id>/', views.GetChatsView.as_view(), name='get_chats'),
    path('chat-interface/', views.ChatInterfaceView.as_view(), name='chat_interface'),
]