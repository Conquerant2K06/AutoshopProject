from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html  # Important !
from .models import UserProfile

# ... le reste du code

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil utilisateur'
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('phone', 'profile_picture', 'address', 'city', 'postal_code')
        }),
    )

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'phone_display']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'profile__phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': (),
            'classes': ('collapse',),
        }),
    )
    
    def phone_display(self, obj):
        if hasattr(obj, 'profile') and obj.profile.phone:
            return obj.profile.phone
        return "Non renseigné"
    phone_display.short_description = 'Téléphone'

# Ré-enregistrer le modèle User avec l'admin personnalisé
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'profile_picture_preview']
    list_filter = ['city']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    readonly_fields = ['profile_picture_preview']
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Coordonnées', {
            'fields': ('phone', 'address', 'city', 'postal_code')
        }),
        ('Photo de profil', {
            'fields': ('profile_picture', 'profile_picture_preview')
        }),
    )
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "Pas de photo"
    profile_picture_preview.short_description = 'Aperçu photo'