from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .models import Categoria, Provincia, Municipio, Empresa
from .serializers import (
    CategoriaSerializer,
    ProvinciaSerializer,
    MunicipioSerializer,
    EmpresaListSerializer,
    EmpresaDetailSerializer,
    EmpresaCreateUpdateSerializer
)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo lectura - Ultraligero"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nombre']
    
    def get_queryset(self):
        cache_key = 'categorias_list'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = list(Categoria.objects.all().order_by('nombre'))
            cache.set(cache_key, queryset, timeout=3600)  # 1 hora
        return queryset


class ProvinciaViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo lectura - Provincias de Cuba"""
    queryset = Provincia.objects.all().order_by('nombre')
    serializer_class = ProvinciaSerializer
    
    def get_queryset(self):
        cache_key = 'provincias_list'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = list(Provincia.objects.all().order_by('nombre'))
            cache.set(cache_key, queryset, timeout=86400)  # 24 horas (no cambia)
        return queryset


class MunicipioViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo lectura - Municipios filtrables por provincia"""
    serializer_class = MunicipioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['provincia']
    
    def get_queryset(self):
        provincia_id = self.request.query_params.get('provincia')
        cache_key = f'municipios_{provincia_id or "all"}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = Municipio.objects.select_related('provincia').all()
            if provincia_id:
                qs = qs.filter(provincia_id=provincia_id)
            queryset = list(qs.order_by('nombre'))
            cache.set(cache_key, queryset, timeout=86400)
        
        return queryset


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    Empresas/Negocios
    
    GET /api/v1/empresas/ - Listar (paginado)
    GET /api/v1/empresas/{slug}/ - Detalle
    POST /api/v1/empresas/ - Crear (auth requerida)
    PUT /api/v1/empresas/{id}/ - Actualizar (auth requerida)
    DELETE /api/v1/empresas/{id}/ - Eliminar (auth requerida)
    """
    queryset = Empresa.objects.select_related(
        'categoria', 'municipio', 'municipio__provincia'
    ).filter(activo=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'municipio', 'provincia']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'creado_en']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmpresaCreateUpdateSerializer
        return EmpresaDetailSerializer
    
    def get_queryset(self):
        """Optimizado con caché y select_related"""
        # Construir cache key basado en filtros
        categoria = self.request.query_params.get('categoria', 'all')
        municipio = self.request.query_params.get('municipio', 'all')
        search = self.request.query_params.get('search', '')
        
        cache_key = f'empresas_{categoria}_{municipio}_{search}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = Empresa.objects.select_related(
                'categoria', 'municipio', 'municipio__provincia'
            ).filter(activo=True)
            
            if categoria != 'all':
                qs = qs.filter(categoria_id=categoria)
            if municipio != 'all':
                qs = qs.filter(municipio_id=municipio)
            if search:
                qs = qs.filter(nombre__icontains=search)
            
            queryset = list(qs.order_by('-creado_en'))
            cache.set(cache_key, queryset, timeout=300)  # 5 minutos
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Detalle de empresa con caché extendido"""
        slug = kwargs.get('slug')
        cache_key = f'empresa_detail_{slug}'
        instance = cache.get(cache_key)
        
        if instance is None:
            instance = self.get_object()
            cache.set(cache_key, instance, timeout=600)  # 10 minutos
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
