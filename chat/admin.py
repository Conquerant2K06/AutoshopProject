# chat/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'participants_count', 'messages_count', 'last_message_preview', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'participants__username']
    filter_horizontal = ['participants']
    list_per_page = 20
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Informations de la salle', {
            'fields': ('name', 'participants', 'is_active')
        }),
        ('Statistiques', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Nombre de participants'
    
    def messages_count(self, obj):
        return obj.messages.count()
    messages_count.short_description = 'Nombre de messages'
    
    def last_message_preview(self, obj):
        last_msg = obj.messages.first()
        if last_msg:
            return format_html(
                '<strong>{}</strong><br><span style="color: #666;">{}</span>',
                last_msg.user.username,
                last_msg.message[:50] + ('...' if len(last_msg.message) > 50 else '')
            )
        return "Aucun message"
    last_message_preview.short_description = 'Dernier message'
    
    actions = ['activate_rooms', 'deactivate_rooms']
    
    def activate_rooms(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} salle(s) activée(s).')
    activate_rooms.short_description = 'Activer les salles sélectionnées'
    
    def deactivate_rooms(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} salle(s) désactivée(s).')
    deactivate_rooms.short_description = 'Désactiver les salles sélectionnées'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'message_preview', 'created_at', 'is_read', 'delete_button']
    list_filter = ['is_read', 'created_at', 'room']
    search_fields = ['user__username', 'message', 'room__name']
    readonly_fields = ['created_at', 'message_full']
    list_per_page = 20
    list_select_related = ['user', 'room']
    
    fieldsets = (
        ('Informations', {
            'fields': ('room', 'user')
        }),
        ('Message', {
            'fields': ('message_full',)
        }),
        ('Statut', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:80] + ('...' if len(obj.message) > 80 else '')
    message_preview.short_description = 'Message'
    
    def message_full(self, obj):
        return format_html(
            '<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #007bff;">'
            '<strong style="color: #007bff;">{}</strong><br>'
            '<span style="white-space: pre-wrap;">{}</span>'
            '</div>',
            obj.user.username,
            obj.message.replace('\n', '<br>')
        )
    message_full.short_description = 'Contenu du message'
    
    def delete_button(self, obj):
        return format_html(
            '<a href="/admin/chat/chatmessage/{}/delete/" '
            'style="background-color: #dc3545; color: white; padding: 5px 10px; '
            'border-radius: 5px; text-decoration: none; display: inline-block;">'
            '🗑️ Supprimer</a>',
            obj.id
        )
    delete_button.short_description = 'Action'
    
    actions = ['mark_as_read', 'mark_as_unread', 'delete_selected_messages']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marqué(s) comme lu(s).')
    mark_as_read.short_description = 'Marquer comme lu'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marqué(s) comme non lu(s).')
    mark_as_unread.short_description = 'Marquer comme non lu'
    
    def delete_selected_messages(self, request, queryset):
        deleted = queryset.count()
        for message in queryset:
            message.delete()
        self.message_user(request, f'{deleted} message(s) supprimé(s).')
    delete_selected_messages.short_description = 'Supprimer les messages sélectionnés'