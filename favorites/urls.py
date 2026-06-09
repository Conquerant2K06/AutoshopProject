from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<int:vehicle_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('list/', views.favorite_list, name='favorite_list'),
    path('count/', views.favorite_count, name='favorite_count'),
]