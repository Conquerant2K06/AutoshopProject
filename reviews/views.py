# reviews/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q  # Ajouter Q ici
from vehicles.models import Vehicle
from .models import Review, ReviewHelpful
from .forms import ReviewForm

@login_required
def add_review(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Vérifier si l'utilisateur a déjà donné son avis
    existing_review = Review.objects.filter(vehicle=vehicle, user=request.user).first()
    
    if request.method == 'POST':
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.vehicle = vehicle
            review.user = request.user
            review.save()
            messages.success(request, 'Votre avis a été publié avec succès !')
            return redirect('vehicle_detail', pk=vehicle_id)
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'vehicle': vehicle,
        'existing_review': existing_review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    vehicle_id = review.vehicle.id
    review.delete()
    messages.success(request, 'Votre avis a été supprimé.')
    return redirect('vehicle_detail', pk=vehicle_id)

@login_required
def helpful_vote(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    vote, created = ReviewHelpful.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'is_helpful': True}
    )
    
    if not created:
        vote.delete()
        is_helpful = False
    else:
        is_helpful = True
    
    helpful_count = review.helpful_votes.count()
    
    return JsonResponse({
        'helpful_count': helpful_count,
        'is_helpful': is_helpful
    })

def get_vehicle_reviews(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    reviews = Review.objects.filter(vehicle=vehicle, is_approved=True)
    
    stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id'),
        rating_5=Count('id', filter=Q(rating=5)),
        rating_4=Count('id', filter=Q(rating=4)),
        rating_3=Count('id', filter=Q(rating=3)),
        rating_2=Count('id', filter=Q(rating=2)),
        rating_1=Count('id', filter=Q(rating=1)),
    )
    
    return JsonResponse({
        'reviews': list(reviews.values('id', 'user__username', 'rating', 'title', 'comment', 'created_at')),
        'stats': stats
    })