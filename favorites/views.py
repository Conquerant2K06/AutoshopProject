# favorites/views.py
from django.shortcuts import get_object_or_404, redirect, render  # Ajouter render ici
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from vehicles.models import Vehicle
from .models import Favorite

@login_required
def toggle_favorite(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vehicle=vehicle)
    
    if not created:
        favorite.delete()
        is_favorite = False
        messages.success(request, f'{vehicle.brand.name} {vehicle.model} retiré des favoris.')
    else:
        is_favorite = True
        messages.success(request, f'{vehicle.brand.name} {vehicle.model} ajouté aux favoris.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})
    
    return redirect(request.META.get('HTTP_REFERER', f'/vehicles/vehicle/{vehicle_id}/'))

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})

@login_required
def favorite_count(request):
    count = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})