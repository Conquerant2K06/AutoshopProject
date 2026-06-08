# utils/email_utils.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_welcome_email(user):
    """Envoyer un email de bienvenue après inscription"""
    subject = 'Bienvenue sur AutoShop ! 🚗'
    
    # Template HTML
    html_content = render_to_string('emails/welcome_email.html', {
        'user': user,
        'site_url': 'http://127.0.0.1:8000',
        'year': 2024
    })
    
    # Version texte
    text_content = strip_tags(html_content)
    
    # Envoyer l'email
    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )

def send_login_notification(user, request):
    """Envoyer une notification de connexion"""
    subject = 'Nouvelle connexion à votre compte AutoShop 🔐'
    
    # Récupérer l'IP et le navigateur
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', 'Inconnu')
    
    html_content = render_to_string('emails/login_notification.html', {
        'user': user,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'login_time': request.session.get('login_time'),
        'site_url': 'http://127.0.0.1:8000'
    })
    
    text_content = strip_tags(html_content)
    
    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )

def send_order_confirmation(order):
    """Envoyer une confirmation de commande"""
    subject = f'Confirmation de votre commande #{order.id} - AutoShop ✅'
    
    html_content = render_to_string('emails/order_confirmation.html', {
        'order': order,
        'vehicle': order.vehicle,
        'user': order.user,
        'site_url': 'http://127.0.0.1:8000',
        'year': 2024
    })
    
    text_content = strip_tags(html_content)
    
    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        html_message=html_content,
        fail_silently=False,
    )

def send_payment_confirmation(payment):
    """Envoyer une confirmation de paiement"""
    subject = f'Paiement confirmé pour la commande #{payment.order.id} - AutoShop 💳'
    
    html_content = render_to_string('emails/payment_confirmation.html', {
        'payment': payment,
        'order': payment.order,
        'user': payment.order.user,
        'site_url': 'http://127.0.0.1:8000',
        'year': 2024
    })
    
    text_content = strip_tags(html_content)
    
    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[payment.order.user.email],
        html_message=html_content,
        fail_silently=False,
    )

def send_order_status_update(order):
    """Envoyer une notification de changement de statut de commande"""
    status_messages = {
        'PENDING': 'en attente de validation',
        'CONFIRMED': 'confirmée',
        'PROCESSING': 'en cours de traitement',
        'COMPLETED': 'terminée',
        'CANCELLED': 'annulée'
    }
    
    subject = f'Mise à jour de votre commande #{order.id} - AutoShop 📦'
    
    html_content = render_to_string('emails/order_status_update.html', {
        'order': order,
        'status_message': status_messages.get(order.status, order.status),
        'user': order.user,
        'site_url': 'http://127.0.0.1:8000'
    })
    
    text_content = strip_tags(html_content)
    
    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        html_message=html_content,
        fail_silently=False,
    )

def get_client_ip(request):
    """Récupérer l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip