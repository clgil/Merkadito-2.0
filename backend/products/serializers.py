from rest_framework import serializers
from .models import Producto


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion_corta', 'precio', 'moneda',
            'imagen', 'categoria', 'disponible', 'empresa_nombre'
        ]


class ProductoDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    empresa = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion_corta', 'precio', 'moneda',
            'imagen', 'categoria', 'disponible', 'empresa',
            'creado_en', 'actualizado_en'
        ]
    
    def get_empresa(self, obj):
        return {
            'id': obj.empresa.id,
            'nombre': obj.empresa.nombre,
            'slug': obj.empresa.slug,
            'whatsapp': obj.empresa.whatsapp,
        }


class ProductoCreateUpdateSerializer(serializers.ModelSerializer):
    """Para crear/actualizar productos"""
    
    class Meta:
        model = Producto
        fields = [
            'empresa', 'nombre', 'descripcion_corta', 'precio', 'moneda',
            'imagen', 'categoria', 'disponible'
        ]