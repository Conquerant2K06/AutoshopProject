# chat/views.py - Version avec AJAX
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ChatRoom, ChatMessage
from django.contrib.auth.models import User

@login_required
def chat_room(request, room_name='support'):
    # Créer ou récupérer la salle de chat
    room, created = ChatRoom.objects.get_or_create(
        name=room_name,
        defaults={'is_active': True}
    )
    
    if created:
        # Ajouter l'admin et l'utilisateur comme participants
        admin = User.objects.filter(is_staff=True).first()
        if admin:
            room.participants.add(admin)
        room.participants.add(request.user)
    
    # Récupérer les messages
    messages_list = ChatMessage.objects.filter(room=room).order_by('created_at')[:100]
    
    # Marquer les messages comme lus
    messages_list.filter(is_read=False).exclude(user=request.user).update(is_read=True)
    
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages_list,
        'room_name': room_name
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message_ajax(request):
    """API pour envoyer un message via AJAX"""
    try:
        data = json.loads(request.body)
        room_name = data.get('room_name', 'support')
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message vide'}, status=400)
        
        # Récupérer la salle
        room, created = ChatRoom.objects.get_or_create(
            name=room_name,
            defaults={'is_active': True}
        )
        
        if created:
            admin = User.objects.filter(is_staff=True).first()
            if admin:
                room.participants.add(admin)
            room.participants.add(request.user)
        
        # Créer le message
        message = ChatMessage.objects.create(
            room=room,
            user=request.user,
            message=message_text
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'username': request.user.username,
            'message': message.message,
            'created_at': message.created_at.strftime('%H:%M')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_messages_ajax(request, room_name='support'):
    """API pour récupérer les messages via AJAX"""
    room = get_object_or_404(ChatRoom, name=room_name)
    messages_list = ChatMessage.objects.filter(room=room).order_by('created_at')[:100]
    
    # Marquer comme lus
    messages_list.filter(is_read=False).exclude(user=request.user).update(is_read=True)
    
    data = []
    for msg in messages_list:
        data.append({
            'id': msg.id,
            'username': msg.user.username,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_mine': msg.user == request.user
        })
    
    return JsonResponse({'messages': data})

@login_required
def get_unread_count(request):
    """API pour obtenir le nombre de messages non lus"""
    rooms = ChatRoom.objects.filter(participants=request.user)
    unread_count = ChatMessage.objects.filter(
        room__in=rooms,
        is_read=False
    ).exclude(user=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})