# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from vehicles.models import Vehicle
from .models import Order, Payment
from .forms import OrderForm
from utils.email_utils import send_order_confirmation, send_payment_confirmation

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
            
            return redirect('payment_process', order_id=order.id)
    else:
        form = OrderForm(initial={
            'delivery_address': request.user.profile.address,
            'delivery_city': request.user.profile.city,
            'delivery_postal_code': request.user.profile.postal_code,
        })
    
    return render(request, 'orders/create_order.html', {
        'form': form,
        'vehicle': vehicle
    })

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Simuler un paiement (à remplacer par Stripe ou autre)
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            is_successful=True
        )
        
        order.status = 'CONFIRMED'
        order.save()
        
        # Envoyer les emails de confirmation
        try:
            send_order_confirmation(order)
            send_payment_confirmation(payment)
            messages.success(request, 'Paiement effectué avec succès ! Un email de confirmation vous a été envoyé.')
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")
            messages.success(request, 'Paiement effectué avec succès !')
        
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'orders/payment.html', {'order': order})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})