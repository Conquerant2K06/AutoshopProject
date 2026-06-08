# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import OrderViewSet, UserViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Pages web
    path('create/<int:vehicle_id>/', views.create_order, name='create_order'),
    path('payment/<int:order_id>/', views.payment_process, name='payment_process'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # API
    path('api/', include(router.urls)),
]