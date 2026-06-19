from django.urls import path
from . import views

urlpatterns = [
    # Registrar click a WhatsApp
    path('click/', views.registrar_click_whatsapp, name='registrar_click_whatsapp'),
    
    # Registrar vista a empresa
    path('vista-empresa/', views.registrar_vista_empresa, name='registrar_vista_empresa'),
    
    # Registrar vista a producto
    path('vista-producto/', views.registrar_vista_producto, name='registrar_vista_producto'),
    
    # Obtener estadísticas de empresa
    path('estadisticas/<int:empresa_id>/', views.estadisticas_empresa, name='estadisticas_empresa'),
]
