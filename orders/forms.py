# orders/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_city', 'delivery_postal_code', 'payment_method']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'delivery_city': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select', 'id': 'payment-method'}, choices=[
                ('CARTE', '💳 Carte bancaire (Stripe)'),
                ('ORANGE_MONEY', '📱 Orange Money'),
                ('MTN_MOMO', '📱 MTN Mobile Money'),
            ]),
        }