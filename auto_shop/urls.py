# auto_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import custom_login  # Importez la nouvelle vue

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vehicles.urls')),
    path('accounts/login/', custom_login, name='login'),  # Utilisez la vue personnalisée
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),  # Ajoutez les URLs de l'application de paiement
    path('chat/', include('chat.urls')),
    path('reviews/', include('reviews.urls')),
    path('favorites/', include('favorites.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)