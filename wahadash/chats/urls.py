from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    # Vamos adicionar URLs aqui depois
    path('history/<int:instance_id>/<str:chat_id>/', views.ChatHistoryView.as_view(), name='chat_history'),
]