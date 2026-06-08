# vehicles/api_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Brand, Vehicle
from .serializers import BrandSerializer, VehicleSerializer, VehicleCreateUpdateSerializer

class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD complet pour les marques
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]  # Temporaire, à restreindre plus tard
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def create(self, request, *args, **kwargs):
        """Créer une nouvelle marque"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Marque créée avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Mettre à jour une marque"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Marque mise à jour',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Supprimer une marque"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 'success',
            'message': 'Marque supprimée'
        }, status=status.HTTP_204_NO_CONTENT)

class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD complet pour les véhicules
    """
    queryset = Vehicle.objects.all()
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VehicleCreateUpdateSerializer
        return VehicleSerializer
    
    def list(self, request, *args, **kwargs):
        """Lister tous les véhicules"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filtres optionnels
        brand = request.query_params.get('brand')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        fuel_type = request.query_params.get('fuel_type')
        condition = request.query_params.get('condition')
        
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if condition:
            queryset = queryset.filter(condition=condition)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """Créer un nouveau véhicule"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Véhicule ajouté avec succès',
                'data': VehicleSerializer(vehicle).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        """Récupérer un véhicule spécifique"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Mettre à jour un véhicule"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Véhicule mis à jour',
                'data': VehicleSerializer(vehicle).data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Supprimer un véhicule"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 'success',
            'message': 'Véhicule supprimé'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Créer plusieurs véhicules en une seule requête"""
        vehicles_data = request.data
        if not isinstance(vehicles_data, list):
            return Response({
                'status': 'error',
                'message': 'Envoyez une liste de véhicules'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created = []
        errors = []
        
        for data in vehicles_data:
            serializer = VehicleCreateUpdateSerializer(data=data)
            if serializer.is_valid():
                vehicle = serializer.save()
                created.append(VehicleSerializer(vehicle).data)
            else:
                errors.append({
                    'data': data,
                    'errors': serializer.errors
                })
        
        return Response({
            'status': 'success',
            'created_count': len(created),
            'created': created,
            'errors': errors
        })

@api_view(['GET'])
def api_root(request):
    """Root de l'API"""
    return Response({
        'brands': '/api/brands/',
        'vehicles': '/api/vehicles/',
        'orders': '/api/orders/',
        'users': '/api/users/',
        'docs': '/api/docs/'
    })