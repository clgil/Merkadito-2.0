from django.urls import path, include

urlpatterns = [
    # Health check
    path('health/', lambda request: __import__('json').dumps({'status': 'ok'}), name='health'),
    
    # Businesses endpoints
    path('', include('businesses.urls')),
    
    # Products endpoints
    path('', include('products.urls')),
    
    # Analytics endpoints (Fase 5 - WhatsApp Centric)
    path('analytics/', include('analytics.urls')),
]
