# vehicles/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import BrandViewSet, VehicleViewSet, api_root

router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

urlpatterns = [
    # Pages web
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('faq/', views.faq, name='faq'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    
    # API
    path('api/', api_root, name='api_root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]