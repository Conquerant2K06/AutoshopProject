from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Vehicle(models.Model):
    FUEL_TYPES = [
        ('ESSENCE', 'Essence'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIQUE', 'Électrique'),
        ('HYBRIDE', 'Hybride'),
    ]
    
    TRANSMISSION_TYPES = [
        ('MANUAL', 'Manuelle'),
        ('AUTOMATIC', 'Automatique'),
    ]
    
    CONDITION_TYPES = [
        ('NEW', 'Neuf'),
        ('USED', 'Occasion'),
    ]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='vehicles')
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.IntegerField(help_text="Kilométrage", null=True, blank=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES)
    condition = models.CharField(max_length=20, choices=CONDITION_TYPES, default='USED')
    color = models.CharField(max_length=50)
    description = models.TextField()
    features = models.TextField(help_text="Caractéristiques séparées par des virgules")
    images = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('vehicle_detail', args=[str(self.id)])
    
    def feature_list(self):
        return [f.strip() for f in self.features.split(',')]
    
    class Meta:
        ordering = ['-created_at']

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='vehicles/')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.vehicle}"