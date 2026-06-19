from rest_framework import serializers
from .models import Categoria, Provincia, Municipio, ConsejoPopular, Barrio, Empresa


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'slug', 'icono']


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ['id', 'nombre']


class MunicipioSerializer(serializers.ModelSerializer):
    provincia_nombre = serializers.CharField(source='provincia.nombre', read_only=True)
    
    class Meta:
        model = Municipio
        fields = ['id', 'nombre', 'provincia', 'provincia_nombre', 'latitud', 'longitud']


class ConsejoPopularSerializer(serializers.ModelSerializer):
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    
    class Meta:
        model = ConsejoPopular
        fields = ['id', 'nombre', 'municipio', 'municipio_nombre', 'codigo']


class BarrioSerializer(serializers.ModelSerializer):
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    consejo_popular_nombre = serializers.CharField(source='consejo_popular.nombre', read_only=True)
    
    class Meta:
        model = Barrio
        fields = ['id', 'nombre', 'municipio', 'consejo_popular', 'municipio_nombre', 'consejo_popular_nombre', 'latitud', 'longitud', 'referencia']


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    provincia_nombre = serializers.CharField(source='municipio.provincia.nombre', read_only=True)
    barrio_nombre = serializers.CharField(source='barrio.nombre', read_only=True)
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'whatsapp', 'categoria_nombre',
            'municipio_nombre', 'provincia_nombre', 'barrio_nombre',
            'logo', 'activo', 'verificado', 'latitud', 'longitud'
        ]


class EmpresaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    categoria = CategoriaSerializer(read_only=True)
    municipio = MunicipioSerializer(read_only=True)
    consejo_popular = ConsejoPopularSerializer(read_only=True)
    barrio = BarrioSerializer(read_only=True)
    whatsapp_link = serializers.SerializerMethodField()
    distancia_km = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'whatsapp', 'telefono', 'direccion',
            'categoria', 'municipio', 'consejo_popular', 'barrio', 'logo',
            'activo', 'verificado', 'whatsapp_link', 'distancia_km',
            'latitud', 'longitud',
            'creado_en', 'actualizado_en'
        ]
    
    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()
    
    def get_distancia_km(self, obj):
        """Calcula distancia desde coordenadas del request (si existen)"""
        request = self.context.get('request')
        if not request or not obj.latitud or not obj.longitud:
            return None
        
        lat_usuario = request.query_params.get('lat')
        lon_usuario = request.query_params.get('lon')
        
        if not lat_usuario or not lon_usuario:
            return None
        
        try:
            from math import radians, sin, cos, sqrt, atan2
            
            R = 6371  # Radio de la Tierra en km
            
            lat1, lon1 = radians(float(lat_usuario)), radians(float(lon_usuario))
            lat2, lon2 = radians(float(obj.latitud)), radians(float(obj.longitud))
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            
            distancia = R * c
            return round(distancia, 2)
        except:
            return None


class EmpresaCreateUpdateSerializer(serializers.ModelSerializer):
    """Para crear/actualizar empresas"""
    
    class Meta:
        model = Empresa
        fields = [
            'nombre', 'descripcion',
            'whatsapp', 'telefono', 'direccion',
            'categoria', 'provincia', 'municipio', 'consejo_popular', 'barrio',
            'latitud', 'longitud',
            'logo', 'activo'
        ]
    
    def validate_whatsapp(self, value):
        numero_limpio = value.replace('+', '').replace(' ', '').replace('-', '')
        if not numero_limpio.isdigit():
            raise serializers.ValidationError('El número de WhatsApp debe contener solo dígitos')
        if len(numero_limpio) < 8:
            raise serializers.ValidationError('Número de WhatsApp inválido')
        return value
