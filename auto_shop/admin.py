# auto_shop/admin.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(AdminSite):
    site_title = _('AutoShop Administration')
    site_header = _('AutoShop - Gestion des ventes de véhicules')
    index_title = _('Tableau de bord')
    
    def get_app_list(self, request):
        """
        Retourne une liste d'applications triée et organisée
        """
        app_list = super().get_app_list(request)
        
        # Personnaliser l'ordre des applications
        app_order = ['vehicles', 'orders', 'accounts', 'auth']
        app_dict = {app['app_label']: app for app in app_list}
        
        ordered_app_list = []
        for app_label in app_order:
            if app_label in app_dict:
                ordered_app_list.append(app_dict[app_label])
        
        # Ajouter les applications restantes
        for app in app_list:
            if app['app_label'] not in app_order:
                ordered_app_list.append(app)
        
        return ordered_app_list

# Créer une instance de l'admin personnalisé
admin_site = CustomAdminSite(name='myadmin')