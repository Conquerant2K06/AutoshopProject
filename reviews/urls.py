from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:vehicle_id>/', views.add_review, name='add_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('helpful/<int:review_id>/', views.helpful_vote, name='helpful_vote'),
    path('api/<int:vehicle_id>/', views.get_vehicle_reviews, name='get_vehicle_reviews'),
]