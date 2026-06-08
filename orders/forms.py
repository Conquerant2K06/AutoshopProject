# orders/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_city', 'delivery_postal_code', 'payment_method']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'payment_method': forms.Select(choices=[
                ('CARTE', 'Carte bancaire'),
                ('PAYPAL', 'PayPal'),
                ('VIREMENT', 'Virement bancaire'),
            ]),
        }