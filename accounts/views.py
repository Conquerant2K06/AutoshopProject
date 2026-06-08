# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm
from orders.models import Order
from utils.email_utils import send_welcome_email, send_login_notification

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Envoyer email de bienvenue
            try:
                send_welcome_email(user)
                messages.success(request, 'Inscription réussie ! Un email de bienvenue vous a été envoyé.')
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")
                messages.success(request, 'Inscription réussie ! Bienvenue sur AutoShop !')
            
            return redirect('vehicle_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """Affiche le profil de l'utilisateur avec ses commandes"""
    return render(request, 'accounts/profile.html')

@login_required
def my_orders(request):
    """Affiche toutes les commandes de l'utilisateur"""
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'accounts/my_orders.html', {'orders': orders})

def custom_logout(request):
    """Déconnexion personnalisée"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès !')
    return redirect('vehicle_list')

def custom_login(request):
    """Vue de connexion personnalisée avec notification par email"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Envoyer notification de connexion
            try:
                send_login_notification(user, request)
                messages.success(request, f'Bienvenue {user.username} ! Un email de notification a été envoyé.')
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")
                messages.success(request, f'Bienvenue {user.username} !')
            
            return redirect('vehicle_list')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'accounts/login.html')