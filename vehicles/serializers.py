# vehicles/serializers.py
from rest_framework import serializers
from .models import Brand, Vehicle, VehicleImage

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'logo']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        if Brand.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f"La marque '{value}' existe déjà")
        return value

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'is_main']

class VehicleSerializer(serializers.ModelSerializer):
    brand_details = BrandSerializer(source='brand', read_only=True)
    images_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'brand', 'brand_details', 'model', 'year', 'price',
            'mileage', 'fuel_type', 'transmission', 'condition',
            'color', 'description', 'features', 'images', 'images_url',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_images_url(self, obj):
        if obj.images:
            return obj.images.url
        return None
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être supérieur à 0")
        return value
    
    def validate_year(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(f"Année invalide (1900-{current_year+1})")
        return value

class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et mise à jour"""
    class Meta:
        model = Vehicle
        fields = '__all__'
    
    def validate_brand(self, value):
        if not value:
            raise serializers.ValidationError("La marque est requise")
        return value