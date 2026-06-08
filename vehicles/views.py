# vehicles/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Vehicle, Brand

def home(request):
    """Page d'accueil moderne"""
    featured_vehicles = Vehicle.objects.filter(is_available=True).order_by('-created_at')[:6]
    best_offers = Vehicle.objects.filter(is_available=True).order_by('price')[:4]
    recent_vehicles = Vehicle.objects.filter(is_available=True).order_by('-created_at')[:8]
    popular_brands = Brand.objects.annotate(
        vehicle_count=Count('vehicles')
    ).filter(vehicle_count__gt=0).order_by('-vehicle_count')[:8]
    
    stats = {
        'total_vehicles': Vehicle.objects.filter(is_available=True).count(),
        'total_brands': Brand.objects.count(),
        'happy_customers': 1250,
        'years_experience': 10,
    }
    
    context = {
        'featured_vehicles': featured_vehicles,
        'best_offers': best_offers,
        'recent_vehicles': recent_vehicles,
        'popular_brands': popular_brands,
        'stats': stats,
    }
    return render(request, 'vehicles/home.html', context)

def about(request):
    """Page À propos"""
    return render(request, 'vehicles/about.html')

def contact(request):
    """Page Contact"""
    return render(request, 'vehicles/contact.html')

def services(request):
    """Page Services"""
    return render(request, 'vehicles/services.html')

def faq(request):
    """Page FAQ"""
    return render(request, 'vehicles/faq.html')

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Vehicle.objects.filter(is_available=True)
        
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        fuel_type = self.request.GET.get('fuel_type')
        transmission = self.request.GET.get('transmission')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('search')
        
        if brand:
            queryset = queryset.filter(brand__name=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        if condition:
            queryset = queryset.filter(condition=condition)
        if search:
            queryset = queryset.filter(
                Q(brand__name__icontains=search) |
                Q(model__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['fuel_choices'] = Vehicle.FUEL_TYPES
        context['transmission_choices'] = Vehicle.TRANSMISSION_TYPES
        return context

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_vehicles'] = Vehicle.objects.filter(
            brand=self.object.brand,
            is_available=True
        ).exclude(id=self.object.id)[:4]
        return context