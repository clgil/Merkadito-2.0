from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import ClickWhatsApp, VistaEmpresa, VistaProducto


@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_click_whatsapp(request):
    """Registrar click a WhatsApp"""
    empresa_id = request.data.get('empresa_id')
    
    if not empresa_id:
        return Response(
            {'error': 'empresa_id requerido'},
            status=400
        )
    
    ClickWhatsApp.objects.create(
        empresa_id=empresa_id,
        ip=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
    
    return Response({'status': 'click registrado'})


@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_vista_empresa(request):
    """Registrar vista a empresa"""
    empresa_id = request.data.get('empresa_id')
    
    if not empresa_id:
        return Response(
            {'error': 'empresa_id requerido'},
            status=400
        )
    
    VistaEmpresa.objects.create(
        empresa_id=empresa_id,
        ip=request.META.get('REMOTE_ADDR')
    )
    
    return Response({'status': 'vista registrada'})


@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_vista_producto(request):
    """Registrar vista a producto"""
    producto_id = request.data.get('producto_id')
    
    if not producto_id:
        return Response(
            {'error': 'producto_id requerido'},
            status=400
        )
    
    VistaProducto.objects.create(
        producto_id=producto_id,
        ip=request.META.get('REMOTE_ADDR')
    )
    
    return Response({'status': 'vista registrada'})


@api_view(['GET'])
@permission_classes([AllowAny])
def estadisticas_empresa(request, empresa_id):
    """Obtener estadísticas básicas de una empresa"""
    desde = request.query_params.get('desde', '30')  # días
    
    fecha_desde = timezone.now() - timedelta(days=int(desde))
    
    clicks = ClickWhatsApp.objects.filter(
        empresa_id=empresa_id,
        fecha__gte=fecha_desde
    ).count()
    
    vistas = VistaEmpresa.objects.filter(
        empresa_id=empresa_id,
        fecha__gte=fecha_desde
    ).count()
    
    return Response({
        'empresa_id': empresa_id,
        'periodo_dias': int(desde),
        'clicks_whatsapp': clicks,
        'vistas_empresa': vistas
    })