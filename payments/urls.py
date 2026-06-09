# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('stripe/<int:order_id>/', views.stripe_payment, name='stripe_payment'),
    path('orange-money/<int:order_id>/', views.orange_money_payment, name='orange_money_payment'),
    path('mtn-momo/<int:order_id>/', views.mtn_momo_payment, name='mtn_momo_payment'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]