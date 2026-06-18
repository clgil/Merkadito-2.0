from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def custom_404(request, exception):
    return Response(
        {'error': 'Recurso no encontrado', 'detail': 'La URL solicitada no existe'},
        status=status.HTTP_404_NOT_FOUND
    )

def custom_500(request):
    return Response(
        {'error': 'Error interno del servidor', 'detail': 'Por favor intenta más tarde'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
