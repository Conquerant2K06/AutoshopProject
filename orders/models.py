from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('PROCESSING', 'En traitement'),
        ('COMPLETED', 'Terminée'),
        ('CANCELLED', 'Annulée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    PAYMENT_METHOD_CHOICES = [
        ('CARTE', 'Carte bancaire'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('MTN_MOMO', 'MTN Mobile Money'),
    ]
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CARTE')
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.vehicle}"
    
    class Meta:
        ordering = ['-order_date']

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_payment_id = models.CharField(max_length=255, blank=True)
    is_successful = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Payment for order {self.order.id}"