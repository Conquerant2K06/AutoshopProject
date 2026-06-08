from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Vehicle, VehicleImage

# Commentez ou supprimez ces imports si vous n'avez pas installé django-admin-rangefilter
# from rangefilter.filters import DateRangeFilter, NumericRangeFilter

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'vehicle_count', 'logo_preview']
    list_filter = ['country']
    search_fields = ['name', 'country']
    fields = ['name', 'country', 'logo']
    
    def vehicle_count(self, obj):
        return obj.vehicles.count()
    vehicle_count.short_description = 'Nombre de véhicules'
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.logo.url)
        return "Pas de logo"
    logo_preview.short_description = 'Aperçu logo'

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 3
    fields = ['image', 'is_main', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'year', 'price_display', 'condition', 'fuel_type', 
                   'transmission', 'is_available', 'created_at', 'thumbnail_preview']
    # Version simplifiée sans rangefilter (commentez les lignes avec rangefilter)
    list_filter = ['brand', 'year', 'fuel_type', 'transmission', 'condition', 'is_available', 'created_at']
    search_fields = ['brand__name', 'model', 'description', 'color']
    list_editable = ['is_available']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'main_image_preview']
    fieldsets = (
        ('Informations de base', {
            'fields': ('brand', 'model', 'year', 'condition')
        }),
        ('Caractéristiques techniques', {
            'fields': ('fuel_type', 'transmission', 'mileage', 'color')
        }),
        ('Prix et description', {
            'fields': ('price', 'description', 'features')
        }),
        ('Statut et images', {
            'fields': ('is_available', 'images', 'main_image_preview')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [VehicleImageInline]
    actions = ['mark_as_available', 'mark_as_unavailable', 'apply_discount']
    
    def get_full_name(self, obj):
        return f"{obj.brand.name} {obj.model}"
    get_full_name.short_description = 'Véhicule'
    get_full_name.admin_order_field = 'model'
    
    def price_display(self, obj):
        return format_html('<b style="color: green;">{:,} FCFA</b>', obj.price)
    price_display.short_description = 'Prix'
    
    def thumbnail_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.images.url)
        return "📷"
    thumbnail_preview.short_description = 'Miniature'
    
    def main_image_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="300" height="200" style="border-radius: 10px;" />', obj.images.url)
        return "Aucune image principale"
    main_image_preview.short_description = 'Aperçu image principale'
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} véhicule(s) marqué(s) comme disponible(s).')
    mark_as_available.short_description = 'Marquer comme disponible'
    
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} véhicule(s) marqué(s) comme indisponible(s).')
    mark_as_unavailable.short_description = 'Marquer comme indisponible'
    
    def apply_discount(self, request, queryset):
        discount = 10
        for vehicle in queryset:
            vehicle.price = vehicle.price * (1 - discount/100)
            vehicle.save()
        self.message_user(request, f'Réduction de {discount}% appliquée à {queryset.count()} véhicule(s).')
    apply_discount.short_description = 'Appliquer 10% de réduction'

@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'is_main', 'image_preview']
    list_filter = ['is_main', 'vehicle__brand']
    search_fields = ['vehicle__brand__name', 'vehicle__model']
    list_editable = ['is_main']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'