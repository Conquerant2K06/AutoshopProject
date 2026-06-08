# orders/api_views.py
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from .models import Order, Payment
from .serializers import OrderSerializer, OrderCreateUpdateSerializer, UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD complet pour les commandes
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """Les utilisateurs normaux voient seulement leurs commandes"""
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        """Lister toutes les commandes"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filtres optionnels
        status_filter = request.query_params.get('status')
        user_id = request.query_params.get('user')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if user_id and request.user.is_staff:
            queryset = queryset.filter(user__id=user_id)
        if date_from:
            queryset = queryset.filter(order_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(order_date__lte=date_to)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """Créer une nouvelle commande"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Commande créée avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annuler une commande"""
        order = self.get_object()
        
        # Vérifier si la commande peut être annulée
        if order.status not in ['PENDING', 'CONFIRMED']:
            return Response({
                'status': 'error',
                'message': 'Cette commande ne peut pas être annulée'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'CANCELLED'
        order.save()
        
        return Response({
            'status': 'success',
            'message': 'Commande annulée avec succès',
            'data': OrderSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirmer une commande (admin seulement)"""
        if not request.user.is_staff:
            return Response({
                'status': 'error',
                'message': 'Non autorisé'
            }, status=status.HTTP_403_FORBIDDEN)
        
        order = self.get_object()
        order.status = 'CONFIRMED'
        order.save()
        
        return Response({
            'status': 'success',
            'message': 'Commande confirmée',
            'data': OrderSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marquer une commande comme terminée (admin seulement)"""
        if not request.user.is_staff:
            return Response({
                'status': 'error',
                'message': 'Non autorisé'
            }, status=status.HTTP_403_FORBIDDEN)
        
        order = self.get_object()
        order.status = 'COMPLETED'
        order.save()
        
        return Response({
            'status': 'success',
            'message': 'Commande marquée comme terminée',
            'data': OrderSerializer(order).data
        })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les utilisateurs (lecture seulement)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Seul l'admin peut voir les utilisateurs
    
    def list(self, request, *args, **kwargs):
        """Lister tous les utilisateurs"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filtres
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search)
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': queryset.count(),
            'data': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """Récupérer les commandes d'un utilisateur spécifique"""
        user = self.get_object()
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'status': 'success',
            'count': orders.count(),
            'data': serializer.data
        })