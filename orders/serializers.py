# orders/serializers.py
from rest_framework import serializers
from .models import Order, Payment
from vehicles.serializers import VehicleSerializer
from django.contrib.auth.models import User
from django.db import models 

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'stripe_payment_id', 'is_successful']
        read_only_fields = ['id', 'payment_date']

class OrderSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    payment_details = PaymentSerializer(source='payment', read_only=True)
    user_name = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'user_email', 'vehicle', 'vehicle_details',
            'order_date', 'status', 'total_amount', 'payment_method',
            'delivery_address', 'delivery_city', 'delivery_postal_code',
            'payment_details'
        ]
        read_only_fields = ['id', 'order_date', 'user']

class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'order_date']

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    full_name = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'is_active', 'date_joined', 'last_login', 'orders_count', 'total_spent'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    
    def get_orders_count(self, obj):
        return obj.orders.count()
    
    def get_total_spent(self, obj):
        total = obj.orders.filter(status='COMPLETED').aggregate(
            total=models.Sum('total_amount')
        )['total']
        return total or 0