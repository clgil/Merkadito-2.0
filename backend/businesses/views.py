from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .models import Categoria, Provincia, Municipio, ConsejoPopular, Barrio, Empresa
from .serializers import (
    CategoriaSerializer,
    ProvinciaSerializer,
    MunicipioSerializer,
    ConsejoPopularSerializer,
    BarrioSerializer,
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


class ConsejoPopularViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo lectura - Consejos Populares filtrables por municipio"""
    serializer_class = ConsejoPopularSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['municipio']
    
    def get_queryset(self):
        municipio_id = self.request.query_params.get('municipio')
        cache_key = f'consejos_populares_{municipio_id or "all"}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = ConsejoPopular.objects.select_related('municipio').all()
            if municipio_id:
                qs = qs.filter(municipio_id=municipio_id)
            queryset = list(qs.order_by('nombre'))
            cache.set(cache_key, queryset, timeout=86400)
        
        return queryset


class BarrioViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo lectura - Barrios filtrables por municipio/consejo popular"""
    serializer_class = BarrioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['municipio', 'consejo_popular']
    
    def get_queryset(self):
        municipio_id = self.request.query_params.get('municipio')
        consejo_id = self.request.query_params.get('consejo_popular')
        cache_key = f'barrios_{municipio_id}_{consejo_id or "all"}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = Barrio.objects.select_related('municipio', 'consejo_popular').all()
            if municipio_id:
                qs = qs.filter(municipio_id=municipio_id)
            if consejo_id:
                qs = qs.filter(consejo_popular_id=consejo_id)
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
    
    Filtros geográficos:
    - ?lat={lat}&lon={lon}&radius={km} - Buscar por radio
    - ?municipio={id} - Filtrar por municipio
    - ?provincia={id} - Filtrar por provincia
    - ?barrio={id} - Filtrar por barrio
    """
    queryset = Empresa.objects.select_related(
        'categoria', 'municipio', 'municipio__provincia'
    ).filter(activo=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'municipio', 'provincia', 'barrio']
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
        provincia = self.request.query_params.get('provincia', 'all')
        barrio = self.request.query_params.get('barrio', 'all')
        search = self.request.query_params.get('search', '')
        lat = self.request.query_params.get('lat', '')
        lon = self.request.query_params.get('lon', '')
        radius = self.request.query_params.get('radius', '')
        
        cache_key = f'empresas_{categoria}_{municipio}_{provincia}_{barrio}_{search}_{lat}_{lon}_{radius}'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            qs = Empresa.objects.select_related(
                'categoria', 'municipio', 'municipio__provincia', 'consejo_popular', 'barrio'
            ).filter(activo=True)
            
            if categoria != 'all':
                qs = qs.filter(categoria_id=categoria)
            if municipio != 'all':
                qs = qs.filter(municipio_id=municipio)
            if provincia != 'all':
                qs = qs.filter(municipio__provincia_id=provincia)
            if barrio != 'all':
                qs = qs.filter(barrio_id=barrio)
            if search:
                qs = qs.filter(nombre__icontains=search)
            
            # Filtrado por coordenadas y radio (geolocalización)
            if lat and lon and radius:
                try:
                    from math import radians, sin, cos, sqrt, atan2
                    
                    R = 6371  # Radio de la Tierra en km
                    lat1, lon1 = radians(float(lat)), radians(float(lon))
                    max_radius = float(radius)
                    
                    # Filtrar empresas que tengan coordenadas
                    qs = qs.exclude(latitud__isnull=True).exclude(longitud__isnull=True)
                    
                    # Filtrar manualmente por distancia (más compatible)
                    empresas_con_distancia = []
                    for empresa in qs:
                        if empresa.latitud and empresa.longitud:
                            lat2, lon2 = radians(float(empresa.latitud)), radians(float(empresa.longitud))
                            dlat = lat2 - lat1
                            dlon = lon2 - lon1
                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1-a))
                            distancia = R * c
                            if distancia <= max_radius:
                                empresas_con_distancia.append(empresa.pk)
                    
                    qs = qs.filter(pk__in=empresas_con_distancia)
                except:
                    pass
            
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
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def cercanos(self, request):
        """
        Buscar empresas cercanas a una ubicación
        
        GET /api/v1/empresas/cercanos/?lat={lat}&lon={lon}&radius={km}
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = request.query_params.get('radius', '5')  # 5km por defecto
        
        if not lat or not lon:
            return Response(
                {'error': 'Se requieren parámetros lat y lon'},
                status=400
            )
        
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            radius_float = float(radius)
        except ValueError:
            return Response(
                {'error': 'lat, lon y radius deben ser números'},
                status=400
            )
        
        # Reutilizar lógica de filtrado por distancia
        queryset = self.get_queryset()
        
        # Aplicar filtro de distancia
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371
        lat1, lon1 = radians(lat_float), radians(lon_float)
        
        empresas_cercanas = []
        for empresa in queryset:
            if empresa.latitud and empresa.longitud:
                lat2, lon2 = radians(float(empresa.latitud)), radians(float(empresa.longitud))
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distancia = R * c
                
                if distancia <= radius_float:
                    empresas_cercanas.append({
                        'empresa': EmpresaListSerializer(empresa).data,
                        'distancia_km': round(distancia, 2)
                    })
        
        # Ordenar por distancia
        empresas_cercanas.sort(key=lambda x: x['distancia_km'])
        
        return Response({
            'count': len(empresas_cercanas),
            'results': empresas_cercanas,
            'ubicacion': {'lat': lat_float, 'lon': lon_float},
            'radio_km': radius_float
        })
