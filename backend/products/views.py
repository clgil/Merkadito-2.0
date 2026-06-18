from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .models import Producto
from .serializers import (
    ProductoListSerializer,
    ProductoDetailSerializer,
    ProductoCreateUpdateSerializer
)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    Productos
    
    GET /api/v1/productos/ - Listar (paginado)
    GET /api/v1/productos/{id}/ - Detalle
    POST /api/v1/productos/ - Crear (auth requerida)
    PUT /api/v1/productos/{id}/ - Actualizar (auth requerida)
    DELETE /api/v1/productos/{id}/ - Eliminar (auth requerida)
    """
    queryset = Producto.objects.select_related('empresa').filter(disponible=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'categoria', 'disponible']
    search_fields = ['nombre', 'descripcion_corta']
    ordering_fields = ['nombre', 'precio', 'creado_en']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateUpdateSerializer
        return ProductoDetailSerializer
    
    def get_queryset(self):
        """Optimizado con caché"""
        empresa = self.request.query_params.get('empresa', 'all')
        categoria = self.request.query_params.get('categoria', 'all')
        
        cache_key = f'productos_{empresa}_{categoria}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = Producto.objects.select_related('empresa').filter(disponible=True)
            
            if empresa != 'all':
                qs = qs.filter(empresa_id=empresa)
            if categoria != 'all':
                qs = qs.filter(categoria=categoria)
            
            queryset = list(qs.order_by('-creado_en'))
            cache.set(cache_key, queryset, timeout=300)  # 5 minutos
        
        return queryset