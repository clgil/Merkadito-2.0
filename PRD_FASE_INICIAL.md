# Tu Merkadito - Fase Inicial

## Descripción

Directorio comercial y catálogo de productos ultraligero para Cuba, optimizado para:
- Internet lento
- Datos móviles limitados
- Equipos antiguos
- Conexiones inestables

## Arquitectura

### Frontend
- Vue 3 (Vite)
- Pinia (gestión de estado)
- Vue Router
- Tailwind CSS
- PWA (Service Workers + IndexedDB)

### Backend
- Django 4.x
- Django REST Framework
- MySQL/MariaDB
- Redis (caché)

---

## Estructura del Proyecto

```
/workspace
├── backend/          # API Django
│   ├── manage.py
│   ├── requirements.txt
│   └── merkadito/    # Configuración Django
├── frontend/         # Aplicación Vue 3
│   ├── package.json
│   ├── vite.config.js
│   └── src/
└── DEPLOYMENT.md     # Guía de despliegue
```

---

## Características Fase Inicial

### Para Usuarios
- ✅ Búsqueda de negocios y productos
- ✅ Filtrado por categorías
- ✅ Filtrado por ubicación (Provincia/Municipio)
- ✅ Ver información de contacto (WhatsApp)
- ✅ Sistema de favoritos (offline)
- ✅ Funcionamiento offline básico

### Para Negocios
- ✅ Registro de empresa (nombre, logo, descripción, ubicación, teléfono, WhatsApp)
- ✅ Gestión de productos (máx 10 campos)
- ✅ Estadísticas básicas (visitas, clicks WhatsApp)

---

## Modelo de Datos Simplificado

### Empresa (Business)
- id
- nombre
- slug
- descripcion
- logo_url
- categoria
- provincia
- municipio
- whatsapp
- telefono
- direccion
- creado_en
- actualizado_en

### Producto (Product)
- id
- empresa_id (FK)
- nombre
- descripcion_corta
- precio
- moneda (CUP/USD/MLC)
- imagen_url
- categoria
- disponible (boolean)
- creado_en
- actualizado_en

---

## Endpoints API Principales

```
GET    /api/v1/empresas/              # Listar empresas (paginado)
GET    /api/v1/empresas/{slug}/       # Detalle de empresa
GET    /api/v1/productos/             # Listar productos (paginado)
GET    /api/v1/categorias/            # Listar categorías
POST   /api/v1/empresas/              # Crear empresa (auth requerida)
PUT    /api/v1/empresas/{id}/         # Actualizar empresa (auth requerida)
POST   /api/v1/productos/             # Crear producto (auth requerida)
DELETE /api/v1/productos/{id}/        # Eliminar producto (auth requerida)
POST   /api/v1/analytics/click/       # Registrar click a WhatsApp
```

---

## Requisitos Previos

### Backend
- Python 3.9+
- MySQL 8.0+ o MariaDB 10.5+
- Redis 6+

### Frontend
- Node.js 18+
- npm o yarn

---

## Instalación Local

Ver sección "Despliegue Local" en DEPLOYMENT.md

---

## Despliegue en Hostinger

Ver sección "Despliegue en Hostinger" en DEPLOYMENT.md

---

## Optimizaciones para Cuba

1. **Bundle inicial < 300 KB**
2. **Lazy loading** de rutas y componentes
3. **Imágenes WebP** con tamaño máximo 1024px
4. **Caché agresivo** con Service Workers
5. **IndexedDB** para datos offline
6. **Paginación obligatoria** en todos los endpoints
7. **OpenStreetMap + Leaflet** en lugar de Google Maps
8. **Sin dependencias pesadas** innecesarias

---

## Métricas de Éxito

- Primer render < 2 segundos
- Funcionamiento offline completo
- Clicks a WhatsApp como métrica principal
- Consumo de datos < 1MB por sesión típica

---

## Próximas Fases

- Fase 2: PWA Offline completa
- Fase 3: Marketplace ultraligero
- Fase 4: Geolocalización cubana
- Fase 5: Sistema WhatsApp-centric
- Fase 6: Analíticas ligeras
- Fase 7: Tu Merkadito Business
- Fase 8: Tu Merkadito POS (producto independiente)
