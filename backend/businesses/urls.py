from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProvinciaViewSet, MunicipioViewSet, ConsejoPopularViewSet, BarrioViewSet, EmpresaViewSet, PlanViewSet, SuscripcionViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'municipios', MunicipioViewSet, basename='municipio')
router.register(r'consejos-populares', ConsejoPopularViewSet, basename='consejo-popular')
router.register(r'barrios', BarrioViewSet, basename='barrio')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'planes', PlanViewSet, basename='plan')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')

urlpatterns = router.urls
