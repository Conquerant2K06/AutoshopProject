# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from vehicles.models import Vehicle
from .models import Order, Payment
from .forms import OrderForm

@login_required
def create_order(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, is_available=True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.vehicle = vehicle
            order.total_amount = vehicle.price
            order.save()
            
            # Rediriger vers le paiement selon le moyen choisi
            payment_method = form.cleaned_data.get('payment_method')
            
            if payment_method == 'CARTE':
                return redirect('payments:stripe_payment', order_id=order.id)
            elif payment_method == 'ORANGE_MONEY':
                return redirect('payments:orange_money_payment', order_id=order.id)
            elif payment_method == 'MTN_MOMO':
                return redirect('payments:mtn_momo_payment', order_id=order.id)
            else:
                return redirect('payments:stripe_payment', order_id=order.id)
    else:
        # Récupérer les infos du profil utilisateur
        profile = getattr(request.user, 'profile', None)
        initial_data = {}
        if profile:
            initial_data = {
                'delivery_address': profile.address or '',
                'delivery_city': profile.city or '',
                'delivery_postal_code': profile.postal_code or '',
            }
        
        form = OrderForm(initial=initial_data)
    
    return render(request, 'orders/create_order.html', {
        'form': form,
        'vehicle': vehicle
    })

@login_required
def payment_process(request, order_id):
    """Ancienne méthode de paiement (redirige vers Stripe)"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return redirect('payments:stripe_payment', order_id=order.id)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})