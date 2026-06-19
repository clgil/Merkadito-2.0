# 📲 Fase 5 - Sistema WhatsApp Centric - Tu Merkadito

## Descripción

Implementación completa del sistema **WhatsApp-Centric** para Tu Merkadito, optimizado para el contexto cubano. Esta fase convierte a WhatsApp en el motor principal de ventas de la plataforma.

---

## 🎯 Objetivo de la Fase 5

**"Todo debe terminar en WhatsApp"**

Cada interacción en la plataforma debe facilitar que el usuario contacte al negocio через WhatsApp para cerrar la venta.

---

## ✅ Características Implementadas

### Backend (Django)

#### Modelos de Analítica Ligera

1. **ClickWhatsApp** - Registro de clicks a WhatsApp
   - empresa (FK)
   - fecha (auto)
   - ip (opcional)
   - user_agent (limitado a 500 chars)

2. **VistaEmpresa** - Registro de vistas a empresas
   - empresa (FK)
   - fecha (auto)
   - ip (opcional)

3. **VistaProducto** - Registro de vistas a productos
   - producto (FK)
   - fecha (auto)
   - ip (opcional)

#### Endpoints API

```
POST /api/v1/analytics/click/           # Registrar click a WhatsApp
POST /api/v1/analytics/vista-empresa/   # Registrar vista a empresa
POST /api/v1/analytics/vista-producto/  # Registrar vista a producto
GET  /api/v1/analytics/estadisticas/<id>/ # Obtener estadísticas de empresa
```

### Frontend (Vue 3)

#### Botones WhatsApp

Todos los botones de acción redirigen a WhatsApp:

- 📲 **Comprar** → `wa.me/numero?text=Hola, quiero comprar...`
- 📲 **Consultar** → `wa.me/numero?text=Hola, quiero consultar...`
- 📲 **Pedir precio** → `wa.me/numero?text=Hola, quiero saber el precio...`
- 📲 **Ver catálogo** → `wa.me/numero?text=Hola, quiero ver el catálogo...`

#### Registro Automático

Cada click a WhatsApp se registra automáticamente en el backend para métricas.

#### Soporte Offline

Los clicks realizados offline se sincronizan cuando hay conexión.

---

## 📁 Estructura de Archivos

```
/workspace
├── backend/
│   ├── analytics/
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py        # ✅ Creado
│   │   │   └── 0002_initial.py        # ✅ Creado
│   │   ├── __init__.py
│   │   ├── models.py                  # ✅ Modelos ClickWhatsApp, VistaEmpresa, VistaProducto
│   │   ├── views.py                   # ✅ Endpoints de analítica
│   │   ├── urls.py                    # ✅ Rutas de analytics
│   │   └── tasks.py                   # Para tareas Celery (futuro)
│   ├── api/
│   │   ├── urls.py                    # ✅ Incluye analytics.urls
│   │   └── views.py
│   └── merkadito/
│       └── urls.py
│
├── frontend/
│   └── src/
│       ├── components/
│       │   └── EmpresaCard.vue        # ✅ Botón WhatsApp
│       ├── views/
│       │   └── EmpresaView.vue        # ✅ Registro de clicks
│       ├── stores/
│       │   └── offline.js             # ✅ Sincronización offline
│       └── pwa/
│           └── sync.js                # ✅ Sync de analytics
│
└── FASE_5_WHATSAPP_CENTRIC.md         # ✅ Este archivo
```

---

## 🚀 Despliegue Local

### Requisitos Previos

- Python 3.9+
- Node.js 18+
- MySQL 8.0+ o MariaDB 10.5+
- Redis 6+ (opcional para caché)

### Paso 1: Configurar Backend

```bash
cd /workspace/backend

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar Base de Datos

```bash
# Crear base de datos en MySQL/MariaDB
mysql -u root -p

CREATE DATABASE merkadito_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'merkadito_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON merkadito_local.* TO 'merkadito_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 3: Configurar Variables de Entorno

Crear archivo `.env` en `/workspace/backend/`:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-x789xyz123abc
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=merkadito_local
DB_USER=merkadito_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=3306

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS para desarrollo
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Paso 4: Ejecutar Migraciones

```bash
cd /workspace/backend

# Aplicar migraciones (incluye Fase 5 - Analytics)
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### Paso 5: Configurar Frontend

```bash
cd /workspace/frontend

# Instalar dependencias
npm install

# Crear archivo .env
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
echo "VITE_APP_NAME=\"Tu Merkadito\"" >> .env
echo "VITE_APP_VERSION=1.0.0" >> .env
```

### Paso 6: Ejecutar en Desarrollo

**Terminal 1 - Backend:**

```bash
cd /workspace/backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python manage.py runserver
```

Backend disponible en: `http://localhost:8000`

**Terminal 2 - Frontend:**

```bash
cd /workspace/frontend
npm run dev
```

Frontend disponible en: `http://localhost:5173`

### Paso 7: Verificar Instalación

```bash
# Verificar endpoint de health
curl http://localhost:8000/api/v1/health/

# Verificar endpoint de analytics
curl -X POST http://localhost:8000/api/v1/analytics/click/ \
  -H "Content-Type: application/json" \
  -d '{"empresa_id": 1}'
```

---

## 🌐 Despliegue en Hostinger

### Requisitos Hostinger

- Plan **Business Web Hosting** o superior (recomendado)
- O **Cloud Startup** para mejor rendimiento
- Acceso a phpMyAdmin o MySQL remoto
- Acceso SSH (habilitar en hPanel)
- Dominio configurado

### Paso 1: Configurar Base de Datos en Hostinger

1. Ingresar a **hPanel**
2. Ir a **Bases de Datos MySQL**
3. Click en **Crear nueva base de datos**
4. Completar:
   - Nombre: `u123456789_merkadito`
   - Usuario: `u123456789_admin`
   - Contraseña: (generar contraseña segura)
5. Guardar credenciales

### Paso 2: Subir Backend vía FTP/SFTP

Usar FileZilla o similar:

1. Conectar a: `ftp.tu-dominio.com`
2. Usuario: tu usuario de hosting
3. Contraseña: tu contraseña
4. Subir carpeta `backend` a: `/public_html/backend`

### Paso 3: Configurar Python en Hostinger

1. En hPanel, ir a **Configuración Avanzada** → **Aplicación Python**
2. Click en **Crear aplicación**
3. Configurar:
   - Directorio: `/public_html/backend`
   - Archivo de entrada: `passenger_wsgi.py`
   - Versión Python: 3.9 o superior
   - Virtual Environment: Activar

### Paso 4: Configurar passenger_wsgi.py

El archivo ya existe en `/workspace/backend/passenger_wsgi.py`. Asegúrate de actualizar la ruta del intérprete:

```python
import sys
import os

INTERP = os.path.expanduser("/home/u123456789/virtualenvs/merkadito/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
os.chdir(os.path.dirname(__file__))

from merkadito.wsgi import application
```

### Paso 5: Instalar Dependencias en Hostinger

Vía SSH:

```bash
ssh u123456789@tu-dominio.com

cd public_html/backend
virtualenv --python=python3.9 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 6: Configurar Variables de Entorno en Producción

En hPanel → **Configuración Avanzada** → **Editor .htaccess**:

```apache
SetEnv SECRET_KEY 'tu-clave-secreta-de-produccion-muy-larga'
SetEnv DB_NAME 'u123456789_merkadito'
SetEnv DB_USER 'u123456789_admin'
SetEnv DB_PASSWORD 'tu-password-seguro-de-hostinger'
SetEnv DB_HOST 'localhost'
SetEnv DEBUG 'False'
SetEnv ALLOWED_HOSTS 'tu-dominio.com,www.tu-dominio.com'
SetEnv REDIS_HOST 'localhost'
SetEnv REDIS_PORT '6379'
```

### Paso 7: Ejecutar Migraciones en Producción

Vía SSH:

```bash
cd public_html/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### Paso 8: Configurar Dominio

#### DNS en tu registrador de dominio:

```
Tipo: A
Nombre: @
Valor: IP-del-servidor-hostinger
TTL: 14400

Tipo: CNAME
Nombre: www
Valor: tu-dominio.com
TTL: 14400
```

#### Apuntar dominio en Hostinger:

1. hPanel → **Hosting** → **Detalles**
2. **Cambiar dominio**
3. Ingresar tu dominio
4. Guardar cambios

### Paso 9: Build y Subida del Frontend

En tu máquina local:

```bash
cd /workspace/frontend

# Actualizar .env para producción
echo "VITE_API_URL=https://tu-dominio.com/api/v1" > .env.production

# Construir
npm run build

# Subir contenido de dist/ a Hostinger
scp -r dist/* u123456789@tu-dominio.com:public_html/
```

### Paso 10: Configurar Redirección SPA

En `/public_html/.htaccess`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### Paso 11: Instalar SSL (Let's Encrypt)

1. hPanel → **Seguridad** → **SSL**
2. Click en **Instalar SSL** en tu dominio
3. Seleccionar **Let's Encrypt**
4. Click en **Instalar**
5. Esperar 5-10 minutos

### Paso 12: Forzar HTTPS

En `/public_html/.htaccess`:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 🧪 Verificación Post-Despliegue

### Verificar Backend

```bash
# Health check
curl https://tu-dominio.com/api/v1/health/

# Probar endpoint de analytics
curl -X POST https://tu-dominio.com/api/v1/analytics/click/ \
  -H "Content-Type: application/json" \
  -d '{"empresa_id": 1}'
```

### Verificar Frontend

1. Abrir `https://tu-dominio.com` en navegador
2. Verificar que carga en < 2 segundos
3. Hacer clic en botón WhatsApp de una empresa
4. Verificar que se abre WhatsApp correctamente

### Verificar Base de Datos

```bash
ssh u123456789@tu-dominio.com

mysql -u u123456789_admin -p u123456789_merkadito

SHOW TABLES LIKE '%analytics%';
SELECT COUNT(*) FROM analytics_clickwhatsapp;
SELECT COUNT(*) FROM analytics_vistaempresa;
SELECT COUNT(*) FROM analytics_vistaproducto;
```

---

## 📊 Métricas de Éxito Fase 5

### KPIs Principales

1. **Clicks a WhatsApp por día**
   - Meta: 100+ clicks/día después de 1 mes

2. **Tasa de conversión (vista → click)**
   - Meta: 15-25%

3. **Empresas registradas**
   - Meta: 50+ empresas en primer mes

4. **Productos activos**
   - Meta: 500+ productos en primer mes

### Monitoreo

```python
# Desde Django shell
python manage.py shell

>>> from analytics.models import ClickWhatsApp
>>> from django.utils import timezone
>>> from datetime import timedelta

>>> # Clicks últimos 7 días
>>> desde = timezone.now() - timedelta(days=7)
>>> ClickWhatsApp.objects.filter(fecha__gte=desde).count()

>>> # Clicks por empresa
>>> from django.db.models import Count
>>> ClickWhatsApp.objects.values('empresa__nombre').annotate(
...     total=Count('id')
... ).order_by('-total')[:10]
```

---

## 🔧 Troubleshooting

### Error 500 en Backend

```bash
# Revisar logs
tail -f /home/u123456789/logs/errors.log

# Verificar permisos
chmod -R 755 public_html/backend
chown -R u123456789:u123456789 public_html/backend
```

### Error de Conexión a Base de Datos

```bash
# Verificar credenciales
cd public_html/backend
source venv/bin/activate
python manage.py shell

>>> from django.conf import settings
>>> print(settings.DATABASES)

# Verificar que MySQL esté corriendo
systemctl status mysql
```

### Los clicks a WhatsApp no se registran

1. Verificar que el endpoint `/api/v1/analytics/click/` responda:
   ```bash
   curl -X POST https://tu-dominio.com/api/v1/analytics/click/ \
     -H "Content-Type: application/json" \
     -d '{"empresa_id": 1}'
   ```

2. Verificar logs de Django para errores

3. Verificar que CORS esté configurado correctamente en `settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://tu-dominio.com",
       "https://www.tu-dominio.com",
   ]
   ```

### El frontend no carga

```bash
# Limpiar caché del navegador
# Ctrl + Shift + Supr

# Verificar consola del navegador
F12 → Console

# Verificar que API esté accesible
curl https://tu-dominio.com/api/v1/empresas/
```

### Error de CORS

En backend `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]

CORS_ALLOW_CREDENTIALS = True
```

### Imágenes no se cargan

```bash
# Verificar permisos de carpeta media
chmod -R 755 public_html/media
chown -R www-data:www-data public_html/media

# Verificar MEDIA_ROOT en settings.py
print(settings.MEDIA_ROOT)
```

### Build de frontend falla

```bash
# Limpiar node_modules
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Verificar versión de Node
node --version  # Debe ser 18+
npm --version
```

---

## 📈 Optimizaciones para Cuba

### 1. Bundle Inicial < 300 KB

```bash
# Analizar bundle
npm run build
npx vite-bundle-visualizer
```

### 2. Lazy Loading de Rutas

En `frontend/src/router/index.js`:

```javascript
const routes = [
  {
    path: '/',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/empresa/:slug',
    component: () => import('../views/EmpresaView.vue')
  }
]
```

### 3. Caché Agresivo

Service workers ya implementados en `frontend/public/sw.js`.

### 4. IndexedDB para Offline

Ver `frontend/src/pwa/db.js` para implementación.

### 5. Imágenes WebP

Al subir imágenes, el backend las convierte automáticamente:

```python
# En products/models.py
from PIL import Image
import io

def optimize_image(image_file):
    img = Image.open(image_file)
    img_io = io.BytesIO()
    img.save(img_io, format='WEBP', quality=80, max_width=1024)
    return img_io
```

### 6. Paginación Obligatoria

Todos los endpoints usan paginación:

```python
# En views.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

---

## 🎯 Próximos Pasos

### Fase 6 - Analíticas Ligeras (2 semanas)

- Dashboard básico para negocios
- Gráficos simples de visitas y clicks
- Exportación básica a CSV

### Fase 7 - Tu Merkadito Business (4 semanas)

- Panel privado para negocios
- Gestión de productos simplificada
- Estadísticas básicas
- Sistema de suscripción

### Fase 8 - Tu Merkadito POS (8-12 semanas)

- Producto independiente
- Subdominio: `pos.tumerkadito.com`
- Inventario, turnos, ventas
- Reportes básicos

---

## ✅ Checklist de Implementación Fase 5

### Backend

- [x] Modelo `ClickWhatsApp` creado
- [x] Modelo `VistaEmpresa` creado
- [x] Modelo `VistaProducto` creado
- [x] Migraciones generadas (`0001_initial.py`, `0002_initial.py`)
- [x] Views para registrar clicks
- [x] Views para registrar vistas
- [x] Endpoint para obtener estadísticas
- [x] URLs configuradas en `analytics/urls.py`
- [x] URLs incluidas en `api/urls.py`

### Frontend

- [x] Botones WhatsApp en `EmpresaCard.vue`
- [x] Botón WhatsApp en `EmpresaView.vue`
- [x] Función `registrarClick()` implementada
- [x] Sincronización offline en `sync.js`
- [x] Store de offline en `offline.js`

### Documentación

- [x] Este archivo `FASE_5_WHATSAPP_CENTRIC.md`
- [x] Instrucciones de despliegue local
- [x] Instrucciones de despliegue en Hostinger
- [x] Troubleshooting incluido

---

## 📞 Soporte

Para problemas específicos:

1. Revisar logs en hPanel
2. Verificar documentación oficial:
   - Django: https://docs.djangoproject.com
   - Vue 3: https://vuejs.org
   - DRF: https://www.django-rest-framework.org
   - Hostinger: https://www.hostinger.com/tutorials

---

## 📄 Licencia

Este proyecto es propiedad intelectual de Tu Merkadito.

---

**Fecha de implementación:** Junio 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Implementado y listo para producción
