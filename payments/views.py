# payments/views.py
import stripe
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from orders.models import Order, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def stripe_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount),
                currency='xof',
                metadata={
                    'order_id': order.id,
                    'user_id': request.user.id
                },
            )
            
            payment = Payment.objects.create(
                order=order,
                amount=order.total_amount,
                stripe_payment_id=intent.id,
                is_successful=False
            )
            
            return JsonResponse({
                'clientSecret': intent.client_secret,
                'payment_id': payment.id
            })
            
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'payments/stripe_payment.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        try:
            payment = Payment.objects.get(stripe_payment_id=payment_intent['id'])
            payment.is_successful = True
            payment.save()
            
            order = payment.order
            order.status = 'CONFIRMED'
            order.save()
            
            # Envoyer email de confirmation (optionnel)
            from utils.email_utils import send_order_confirmation, send_payment_confirmation
            try:
                send_order_confirmation(order)
                send_payment_confirmation(payment)
            except:
                pass
            
        except Payment.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'success'})

@login_required
def orange_money_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            messages.error(request, 'Veuillez entrer votre numéro Orange Money')
            return render(request, 'payments/orange_money_payment.html', {'order': order})
        
        # Créer le paiement
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            is_successful=True  # Simuler un paiement réussi
        )
        
        order.status = 'CONFIRMED'
        order.save()
        
        messages.success(request, f'Paiement de {order.total_amount} FCFA effectué avec succès via Orange Money !')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'payments/orange_money_payment.html', {'order': order})

@login_required
def mtn_momo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            messages.error(request, 'Veuillez entrer votre numéro MTN Mobile Money')
            return render(request, 'payments/mtn_momo_payment.html', {'order': order})
        
        # Créer le paiement
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            is_successful=True  # Simuler un paiement réussi
        )
        
        order.status = 'CONFIRMED'
        order.save()
        
        messages.success(request, f'Paiement de {order.total_amount} FCFA effectué avec succès via MTN Mobile Money !')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'payments/mtn_momo_payment.html', {'order': order})