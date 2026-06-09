# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/', views.chat_room, name='chat_room'),
    path('api/send-message/', views.send_message_ajax, name='send_message_ajax'),
    path('api/get-messages/<str:room_name>/', views.get_messages_ajax, name='get_messages_ajax'),
    path('api/unread-count/', views.get_unread_count, name='unread_count'),
]