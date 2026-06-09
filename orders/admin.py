from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Order, Payment

class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False
    verbose_name_plural = 'Paiements'
    fields = ['amount', 'payment_date', 'stripe_payment_id', 'is_successful']
    readonly_fields = ['payment_date']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'vehicle_display', 'order_date', 'total_amount_display', 
                   'status', 'payment_status', 'delivery_info']
    list_filter = ['status', 'order_date', 'payment__is_successful']
    search_fields = ['user__username', 'user__email', 'vehicle__brand__name', 'vehicle__model', 'id']
    readonly_fields = ['order_date', 'total_amount']
    date_hierarchy = 'order_date'
    list_per_page = 20
    fieldsets = (
        ('Informations commande', {
            'fields': ('user', 'vehicle', 'order_date', 'status')
        }),
        ('Détails financiers', {
            'fields': ('total_amount', 'payment_method')
        }),
        ('Adresse de livraison', {
            'fields': ('delivery_address', 'delivery_city', 'delivery_postal_code')
        }),
    )
    inlines = [PaymentInline]
    actions = ['confirm_orders', 'complete_orders', 'cancel_orders']
    
    def vehicle_display(self, obj):
        return f"{obj.vehicle.brand.name} {obj.vehicle.model} ({obj.vehicle.year})"
    vehicle_display.short_description = 'Véhicule'
    
    def total_amount_display(self, obj):
        color = 'green' if obj.status == 'COMPLETED' else 'orange'
        formatted_amount = f"{obj.total_amount:,.0f}".replace(',', ' ')
        # Utilisation de mark_safe pour interpréter le HTML
        return mark_safe(f'<b style="color: {color};">{formatted_amount} FCFA</b>')
    total_amount_display.short_description = 'Montant total'
    
    def payment_status(self, obj):
        if hasattr(obj, 'payment') and obj.payment and obj.payment.is_successful:
            return mark_safe('<span style="color: green; font-weight: bold;">✓ Payé</span>')
        return mark_safe('<span style="color: red; font-weight: bold;">✗ Non payé</span>')
    payment_status.short_description = 'Statut paiement'
    
    def delivery_info(self, obj):
        return f"{obj.delivery_city} - {obj.delivery_postal_code}"
    delivery_info.short_description = 'Livraison'
    
    def confirm_orders(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        self.message_user(request, f'{updated} commande(s) confirmée(s).')
    confirm_orders.short_description = 'Confirmer les commandes sélectionnées'
    
    def complete_orders(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f'{updated} commande(s) terminée(s).')
    complete_orders.short_description = 'Terminer les commandes sélectionnées'
    
    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f'{updated} commande(s) annulée(s).')
    cancel_orders.short_description = 'Annuler les commandes sélectionnées'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount_display', 'payment_date', 'is_successful', 'payment_method_display']
    list_filter = ['is_successful', 'payment_date']
    search_fields = ['order__id', 'order__user__username', 'stripe_payment_id']
    readonly_fields = ['payment_date']
    list_editable = ['is_successful']
    
    def amount_display(self, obj):
        color = 'green' if obj.is_successful else 'red'
        formatted_amount = f"{obj.amount:,.0f}".replace(',', ' ')
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{formatted_amount} FCFA</span>')
    amount_display.short_description = 'Montant'
    
    def payment_method_display(self, obj):
        if obj.stripe_payment_id:
            return mark_safe('<span style="color: blue;">💳 Carte bancaire</span>')
        return mark_safe('<span style="color: gray;">💰 Autre</span>')
    payment_method_display.short_description = 'Méthode'