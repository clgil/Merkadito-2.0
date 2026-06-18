from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProvinciaViewSet, MunicipioViewSet, EmpresaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'municipios', MunicipioViewSet, basename='municipio')
router.register(r'empresas', EmpresaViewSet, basename='empresa')

urlpatterns = router.urls
