from rest_framework import serializers
from .models import Categoria, Provincia, Municipio, Empresa


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
        fields = ['id', 'nombre', 'provincia', 'provincia_nombre']


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    provincia_nombre = serializers.CharField(source='municipio.provincia.nombre', read_only=True)
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'whatsapp', 'categoria_nombre',
            'municipio_nombre', 'provincia_nombre',
            'logo', 'activo', 'verificado'
        ]


class EmpresaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    categoria = CategoriaSerializer(read_only=True)
    municipio = MunicipioSerializer(read_only=True)
    whatsapp_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'whatsapp', 'telefono', 'direccion',
            'categoria', 'municipio', 'logo',
            'activo', 'verificado', 'whatsapp_link',
            'creado_en', 'actualizado_en'
        ]


class EmpresaCreateUpdateSerializer(serializers.ModelSerializer):
    """Para crear/actualizar empresas"""
    
    class Meta:
        model = Empresa
        fields = [
            'nombre', 'descripcion',
            'whatsapp', 'telefono', 'direccion',
            'categoria', 'provincia', 'municipio',
            'logo', 'activo'
        ]
    
    def validate_whatsapp(self, value):
        numero_limpio = value.replace('+', '').replace(' ', '').replace('-', '')
        if not numero_limpio.isdigit():
            raise serializers.ValidationError('El número de WhatsApp debe contener solo dígitos')
        if len(numero_limpio) < 8:
            raise serializers.ValidationError('Número de WhatsApp inválido')
        return value
