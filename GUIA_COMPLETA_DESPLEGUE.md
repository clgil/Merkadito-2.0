# 🏪 Tu Merkadito - Guía Completa de Despliegue

**El directorio comercial y catálogo de productos más rápido de Cuba conectado a WhatsApp.**

Tu Merkadito está optimizado para la realidad cubana:
- ✅ Internet lento e inestable
- ✅ Datos móviles limitados
- ✅ Equipos antiguos y móviles de gama baja
- ✅ Apagones frecuentes
- ✅ Funcionamiento offline completo

---

## 📋 Tabla de Contenidos

1. [Estado del Proyecto](#estado-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Despliegue Local](#despliegue-local)
4. [Despliegue en Hostinger](#despliegue-en-hostinger)
5. [Variables de Entorno](#variables-de-entorno)
6. [Troubleshooting](#troubleshooting)
7. [Métricas de Éxito](#métricas-de-éxito)

---

## 🎯 Estado del Proyecto

### Fases Implementadas (Fases 0-5 COMPLETADAS)

| Fase | Descripción | Estado | Características Principales |
|------|-------------|--------|---------------------------|
| **Fase 0** | Optimización del Core | ✅ Completada | Paginación, caché, lazy loading, bundle < 300KB |
| **Fase 1** | Nuevo Diseño UI | ✅ Completada | Tailwind, Shadcn Vue, Dark mode, Responsive |
| **Fase 2** | PWA Offline | ✅ Completada | Service Workers, IndexedDB, Cache First |
| **Fase 3** | Marketplace Ultraligero | ✅ Completada | Empresas y Productos simplificados (≤10 campos) |
| **Fase 4** | Geolocalización Cubana | ✅ Completada | OpenStreetMap, Leaflet, Provincias/Municipios |
| **Fase 5** | Sistema WhatsApp Centric | ✅ Completada | Botones WhatsApp, Analytics de clicks/vistas |

### Próximas Fases

| Fase | Descripción | Duración | Estado |
|------|-------------|----------|--------|
| **Fase 6** | Analíticas Ligeras | 2 semanas | Pendiente |
| **Fase 7** | Tu Merkadito Business | 4 semanas | Pendiente |
| **Fase 8** | Tu Merkadito POS | 8-12 semanas | Pendiente |

---

## 🏗️ Arquitectura

### Stack Tecnológico

#### Backend
- **Framework:** Django 4.2.x + Django REST Framework 3.14+
- **Base de Datos:** MySQL 8.0+ / MariaDB 10.5+
- **Caché:** Redis 6+
- **Servidor WSGI:** Gunicorn / Passenger (Hostinger)
- **Apps:**
  - `businesses` - Gestión de empresas
  - `products` - Gestión de productos
  - `analytics` - Analytics de clicks y vistas (Fase 5)
  - `api` - Endpoints REST

#### Frontend
- **Framework:** Vue 3 (Vite)
- **Estado:** Pinia
- **Router:** Vue Router 4
- **Estilos:** Tailwind CSS
- **HTTP Client:** Axios
- **PWA:** Service Workers + IndexedDB

### Estructura de Directorios

```
/workspace
├── backend/
│   ├── analytics/              # Fase 5 - Analytics
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── 0002_initial.py
│   │   ├── __init__.py
│   │   ├── models.py           # ClickWhatsApp, VistaEmpresa, VistaProducto
│   │   ├── views.py            # Endpoints de analytics
│   │   ├── urls.py             # Rutas de analytics
│   │   └── tasks.py
│   ├── businesses/             # Empresas
│   │   ├── migrations/
│   │   ├── models.py           # Empresa, Categoria
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── products/               # Productos
│   │   ├── migrations/
│   │   ├── models.py           # Producto
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── api/
│   │   ├── urls.py             # Incluye todas las rutas
│   │   └── views.py
│   ├── merkadito/
│   │   ├── settings.py         # Configuración Django
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── manage.py
│   ├── passenger_wsgi.py       # Para Hostinger
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── manifest.json       # PWA Manifest
│   │   ├── sw.js               # Service Worker
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── EmpresaCard.vue      # Card con botón WhatsApp
│   │   │   ├── ProductoCard.vue
│   │   │   ├── Filters.vue
│   │   │   ├── MapaCuba.vue
│   │   │   ├── SearchBar.vue
│   │   │   └── OfflineBanner.vue
│   │   ├── views/
│   │   │   ├── HomeView.vue
│   │   │   ├── EmpresaView.vue     # Registro de clicks
│   │   │   ├── ProductoView.vue
│   │   │   ├── SearchView.vue
│   │   │   ├── FavoritosView.vue
│   │   │   └── OfflineView.vue
│   │   ├── stores/
│   │   │   ├── favorites.js        # Store de favoritos
│   │   │   └── offline.js          # Store de estado offline
│   │   ├── pwa/
│   │   │   ├── db.js               # IndexedDB helpers
│   │   │   └── sync.js             # Sincronización offline
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── assets/
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── README.md
├── DEPLOYMENT.md
├── FASE_5_WHATSAPP_CENTRIC.md
└── PRD_FASE_INICIAL.md
```

---

## 🖥️ Despliegue Local

### Requisitos Previos

- **Python:** 3.9 o superior
- **Node.js:** 18 o superior
- **MySQL:** 8.0+ o MariaDB 10.5+
- **Redis:** 6+ (opcional para caché)
- **Git:** Para clonar el repositorio

### Paso 1: Clonar o Acceder al Proyecto

```bash
cd /workspace
```

### Paso 2: Configurar Backend

#### 2.1 Crear Entorno Virtual

```bash
cd /workspace/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

#### 2.2 Instalar Dependencias

```bash
pip install -r requirements.txt
```

**requirements.txt incluye:**
- Django>=4.2,<5.0
- djangorestframework>=3.14.0
- django-cors-headers>=4.3.0
- django-filter>=23.5
- PyMySQL>=1.1.0
- Pillow>=10.2.0
- redis>=5.0.0
- django-redis>=5.4.0
- python-decouple>=3.8
- gunicorn>=21.2.0
- drf-spectacular>=0.27.0

#### 2.3 Configurar Base de Datos

**Opción A: MySQL/MariaDB**

```bash
# Iniciar sesión en MySQL
mysql -u root -p

# Crear base de datos
CREATE DATABASE merkadito_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Crear usuario (opcional, recomendado para producción)
CREATE USER 'merkadito_user'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON merkadito_local.* TO 'merkadito_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Opción B: SQLite (solo desarrollo)**

Modificar `backend/merkadito/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 2.4 Configurar Variables de Entorno

Crear archivo `.env` en `/workspace/backend/`:

```env
# Seguridad
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-x789xyz123abc

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=merkadito_local
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0

# CORS para desarrollo
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Analytics
ANALYTICS_ENABLED=True
```

#### 2.5 Ejecutar Migraciones

```bash
cd /workspace/backend

# Aplicar migraciones (incluye Fase 5 - Analytics)
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario (opcional)
python manage.py createsuperuser
```

#### 2.6 Verificar Migraciones de Analytics

```bash
python manage.py showmigrations analytics

# Debe mostrar:
# analytics
#  [X] 0001_initial
#  [X] 0002_initial
```

### Paso 3: Configurar Frontend

#### 3.1 Instalar Dependencias

```bash
cd /workspace/frontend

npm install
```

#### 3.2 Configurar Variables de Entorno

Crear archivo `.env` en `/workspace/frontend/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0
VITE_MAX_IMAGE_SIZE=1048576
VITE_CACHE_ENABLED=true
```

#### 3.3 Verificar Componentes Clave

Los siguientes componentes ya están implementados:

- `src/components/EmpresaCard.vue` - Incluye botón WhatsApp con registro de clicks
- `src/views/EmpresaView.vue` - Detalle de empresa con registro de vistas
- `src/pwa/sync.js` - Sincronización offline de analytics
- `src/stores/offline.js` - Gestión de estado offline

### Paso 4: Ejecutar en Desarrollo

#### Terminal 1 - Backend

```bash
cd /workspace/backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python manage.py runserver
```

**Backend disponible en:** `http://localhost:8000`

**Endpoints principales:**
- API Root: `http://localhost:8000/api/v1/`
- Health Check: `http://localhost:8000/api/v1/health/`
- Empresas: `http://localhost:8000/api/v1/empresas/`
- Productos: `http://localhost:8000/api/v1/productos/`
- Analytics Click: `POST http://localhost:8000/api/v1/analytics/click/`
- Admin Django: `http://localhost:8000/admin/`

#### Terminal 2 - Frontend

```bash
cd /workspace/frontend
npm run dev
```

**Frontend disponible en:** `http://localhost:5173`

#### Terminal 3 - Redis (opcional)

```bash
# Ubuntu/Debian
sudo systemctl start redis

# Windows (si está instalado como servicio)
redis-server

# Mac
brew services start redis

# Verificar conexión
redis-cli ping
# Debe responder: PONG
```

### Paso 5: Verificar Instalación

#### Probar Backend

```bash
# Health check
curl http://localhost:8000/api/v1/health/

# Listar empresas
curl http://localhost:8000/api/v1/empresas/

# Registrar click a WhatsApp (simulado)
curl -X POST http://localhost:8000/api/v1/analytics/click/ \
  -H "Content-Type: application/json" \
  -d '{"empresa_id": 1}'
```

#### Probar Frontend

1. Abrir `http://localhost:5173` en navegador
2. Verificar que carga en < 2 segundos
3. Buscar una empresa
4. Hacer clic en botón WhatsApp
5. Verificar en consola del navegador que se registra el click

#### Verificar Service Worker

1. Abrir DevTools (F12)
2. Ir a pestaña Application
3. Verificar Service Worker registrado
4. Verificar IndexedDB con tablas: empresas, productos, sync_actions

---

## 🌐 Despliegue en Hostinger

### Requisitos Hostinger

- **Plan Recomendado:** Business Web Hosting o superior
- **Alternativa:** Cloud Startup para mejor rendimiento
- **Acceso SSH:** Habilitar en hPanel
- **Dominio:** Configurado y apuntando a Hostinger

### Paso 1: Configurar Base de Datos en Hostinger

#### 1.1 Crear Base de Datos

1. Ingresar a **hPanel**
2. Ir a **Bases de Datos MySQL**
3. Click en **Crear nueva base de datos**
4. Completar:
   - Nombre: `u123456789_merkadito`
   - Usuario: `u123456789_admin`
   - Contraseña: (generar contraseña segura de 16+ caracteres)
5. **Guardar credenciales** en gestor de contraseñas

#### 1.2 Anotar Credenciales

```
Database Name: u123456789_merkadito
Username: u123456789_admin
Password: [tu-password-generado]
Host: localhost
Port: 3306
```

### Paso 2: Preparar Backend para Producción

#### 2.1 Modificar settings.py (opcional)

En `/workspace/backend/merkadito/settings.py`, asegurar:

```python
# Línea 12
DEBUG = config('DEBUG', default=False, cast=bool)  # False en producción

# Línea 14
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='tu-dominio.com,www.tu-dominio.com').split(',')
```

#### 2.2 Verificar passenger_wsgi.py

El archivo `/workspace/backend/passenger_wsgi.py` debe estar configurado:

```python
import sys
import os

# Path al virtualenv en Hostinger (ajustar según tu usuario)
INTERP = os.path.expanduser("/home/u123456789/virtualenvs/merkadito/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Agregar el directorio del proyecto al path
sys.path.append(os.getcwd())
os.chdir(os.path.dirname(__file__))

from merkadito.wsgi import application
```

**Importante:** Reemplazar `u123456789` con tu usuario real de Hostinger.

### Paso 3: Subir Backend vía FTP/SFTP

#### 3.1 Usar FileZilla o Similar

1. **Conectar:**
   - Host: `ftp.tu-dominio.com`
   - Usuario: `u123456789` (tu usuario de Hostinger)
   - Contraseña: tu contraseña
   - Puerto: 21 (FTP) o 22 (SFTP)

2. **Subir archivos:**
   - Navegar a `/public_html/`
   - Crear carpeta `backend`
   - Subir TODO el contenido de `/workspace/backend/` a `/public_html/backend/`

#### 3.2 Estructura Resultante

```
/public_html/
└── backend/
    ├── analytics/
    ├── businesses/
    ├── products/
    ├── api/
    ├── merkadito/
    ├── manage.py
    ├── passenger_wsgi.py
    ├── requirements.txt
    └── ...
```

### Paso 4: Configurar Python en Hostinger

#### 4.1 Crear Aplicación Python

1. En hPanel, ir a **Configuración Avanzada** → **Aplicación Python**
2. Click en **Crear aplicación**
3. Configurar:
   - **Directorio:** `/public_html/backend`
   - **Archivo de entrada:** `passenger_wsgi.py`
   - **Versión Python:** 3.9 o superior
   - **Virtual Environment:** Activar (se creará automáticamente)

#### 4.2 Esperar Inicialización

Hostinger creará el entorno virtual automáticamente. Esto puede tomar 2-5 minutos.

### Paso 5: Instalar Dependencias vía SSH

#### 5.1 Habilitar SSH (si no está habilitado)

1. hPanel → **Configuración Avanzada** → **SSH Access**
2. Activar SSH
3. Anotar credenciales SSH

#### 5.2 Conectar vía SSH

```bash
ssh u123456789@tu-dominio.com
# O usar el puerto indicado por Hostinger
ssh -p 65002 u123456789@ssh.hostinger.com
```

#### 5.3 Instalar Dependencias

```bash
# Navegar al backend
cd public_html/backend

# Activar virtualenv (Hostinger lo crea automáticamente)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep Django
# Debe mostrar Django 4.2.x
```

### Paso 6: Configurar Variables de Entorno en Producción

#### Opción A: Usando .htaccess (Recomendado)

En hPanel → **Configuración Avanzada** → **Editor .htaccess**:

```apache
# Variables de entorno para Django
SetEnv SECRET_KEY 'tu-clave-secreta-de-produccion-muy-larga-y-aleatoria-xyz789'
SetEnv DB_NAME 'u123456789_merkadito'
SetEnv DB_USER 'u123456789_admin'
SetEnv DB_PASSWORD 'tu-password-seguro-de-hostinger'
SetEnv DB_HOST 'localhost'
SetEnv DB_PORT '3306'
SetEnv DEBUG 'False'
SetEnv ALLOWED_HOSTS 'tu-dominio.com,www.tu-dominio.com'
SetEnv REDIS_HOST 'localhost'
SetEnv REDIS_PORT '6379'
SetEnv CORS_ALLOWED_ORIGINS 'https://tu-dominio.com,https://www.tu-dominio.com'
SetEnv ANALYTICS_ENABLED 'True'
```

#### Opción B: Usando .env (Alternativa)

Crear archivo `.env` en `/public_html/backend/`:

```env
SECRET_KEY=tu-clave-secreta-de-produccion-muy-larga-y-aleatoria-xyz789
DB_NAME=u123456789_merkadito
DB_USER=u123456789_admin
DB_PASSWORD=tu-password-seguro-de-hostinger
DB_HOST=localhost
DB_PORT=3306
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
ANALYTICS_ENABLED=True
```

### Paso 7: Ejecutar Migraciones en Producción

Vía SSH:

```bash
cd public_html/backend
source venv/bin/activate

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser
```

### Paso 8: Configurar Dominio

#### 8.1 DNS en tu Registrador de Dominio

En el administrador de tu dominio (GoDaddy, Namecheap, etc.):

```
Tipo: A
Nombre: @
Valor: [IP-del-servidor-hostinger]
TTL: 14400

Tipo: CNAME
Nombre: www
Valor: tu-dominio.com
TTL: 14400
```

**Obtener IP de Hostinger:**
- hPanel → **Hosting** → **Detalles del Plan**
- Buscar "IP Address" o "Server IP"

#### 8.2 Apuntar Dominio en Hostinger

1. hPanel → **Hosting** → **Detalles**
2. **Cambiar dominio**
3. Ingresar tu dominio
4. Guardar cambios

**Propagación DNS:** Puede tardar hasta 24-48 horas.

### Paso 9: Build y Subida del Frontend

#### 9.1 Build de Producción en Local

```bash
cd /workspace/frontend

# Crear .env.production
cat > .env.production << EOF
VITE_API_URL=https://tu-dominio.com/api/v1
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0
VITE_MAX_IMAGE_SIZE=1048576
VITE_CACHE_ENABLED=true
EOF

# Construir
npm run build
```

#### 9.2 Subir Build a Hostinger

**Opción A: Vía SCP**

```bash
cd /workspace/frontend
scp -r dist/* u123456789@tu-dominio.com:public_html/
```

**Opción B: Vía FTP (FileZilla)**

1. Conectar a `ftp.tu-dominio.com`
2. Navegar a `/public_html/`
3. Subir TODO el contenido de `dist/` a `/public_html/`

**Estructura resultante:**

```
/public_html/
├── index.html          # Del build de frontend
├── assets/             # JS, CSS del build
├── manifest.json
├── sw.js
├── backend/            # Backend Django
└── .htaccess
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
  
  # Excluir backend Django
  RewriteCond %{REQUEST_URI} !^/backend/
  RewriteCond %{REQUEST_URI} !^/api/
  RewriteCond %{REQUEST_URI} !^/admin/
  RewriteCond %{REQUEST_URI} !^/static/
  RewriteCond %{REQUEST_URI} !^/media/
  
  RewriteRule . /index.html [L]
</IfModule>
```

### Paso 11: Instalar SSL (Let's Encrypt)

1. hPanel → **Seguridad** → **SSL**
2. Click en **Instalar SSL** en tu dominio
3. Seleccionar **Let's Encrypt** (gratuito)
4. Click en **Instalar**
5. Esperar 5-10 minutos

### Paso 12: Forzar HTTPS

En `/public_html/.htaccess`, agregar al inicio:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 🔧 Variables de Entorno

### Backend (.env o hPanel)

```env
# ===========================
# SEGURIDAD
# ===========================
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-minimo-50-caracteres-xyz789abc
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# ===========================
# BASE DE DATOS
# ===========================
DB_NAME=u123456789_merkadito
DB_USER=u123456789_admin
DB_PASSWORD=password-seguro-de-16-caracteres-minimo
DB_HOST=localhost
DB_PORT=3306

# ===========================
# REDIS (CACHE)
# ===========================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0

# ===========================
# CORS
# ===========================
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
CORS_ALLOW_CREDENTIALS=True

# ===========================
# ARCHIVOS MULTIMEDIA
# ===========================
MEDIA_ROOT=/home/u123456789/public_html/media
MEDIA_URL=https://tu-dominio.com/media/

# ===========================
# EMAIL (OPCIONAL)
# ===========================
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# ===========================
# ANALYTICS
# ===========================
ANALYTICS_ENABLED=True

# ===========================
# OPTIMIZACIÓN PARA CUBA
# ===========================
MAX_UPLOAD_SIZE=1048576
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
```

### Frontend (.env.production)

```env
# API URL
VITE_API_URL=https://tu-dominio.com/api/v1

# Información de la App
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0

# Optimización
VITE_MAX_IMAGE_SIZE=1048576
VITE_CACHE_ENABLED=true
VITE_OFFLINE_ENABLED=true
```

---

## 🐛 Troubleshooting

### Error 500 en Backend

#### Síntomas
- Página en blanco
- Error "Internal Server Error"

#### Solución

```bash
# 1. Revisar logs de error
tail -f /home/u123456789/logs/errors.log

# 2. Verificar permisos
chmod -R 755 public_html/backend
chown -R u123456789:u123456789 public_html/backend

# 3. Verificar passenger_wsgi.py
cat public_html/backend/passenger_wsgi.py

# Asegurar que la ruta INTERP sea correcta
# INTERP = os.path.expanduser("/home/u123456789/virtualenvs/merkadito/bin/python")
```

### Error de Conexión a Base de Datos

#### Síntomas
- Error "Can't connect to MySQL server"
- Error "Access denied for user"

#### Solución

```bash
# 1. Verificar credenciales en .htaccess o .env
# DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

# 2. Probar conexión manual
mysql -u u123456789_admin -p u123456789_merkadito

# 3. Verificar que MySQL esté corriendo
systemctl status mysql

# 4. Desde Django shell
cd public_html/backend
source venv/bin/activate
python manage.py shell

>>> from django.conf import settings
>>> print(settings.DATABASES)
```

### Los Clicks a WhatsApp no se Registran

#### Síntomas
- Botón WhatsApp funciona
- No hay registros en tabla `analytics_clickwhatsapp`

#### Solución

```bash
# 1. Verificar endpoint
curl -X POST https://tu-dominio.com/api/v1/analytics/click/ \
  -H "Content-Type: application/json" \
  -d '{"empresa_id": 1}'

# Debe responder: {"status": "click registrado"}

# 2. Verificar logs de Django
tail -f /home/u123456789/logs/errors.log | grep analytics

# 3. Verificar CORS en settings.py
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]

# 4. Verificar migraciones de analytics
python manage.py showmigrations analytics
# Deben estar todas marcadas con [X]
```

### El Frontend no Carga

#### Síntomas
- Pantalla en blanco
- Error de consola

#### Solución

```bash
# 1. Limpiar caché del navegador
# Ctrl + Shift + Supr

# 2. Verificar consola del navegador
F12 → Console

# 3. Verificar que API esté accesible
curl https://tu-dominio.com/api/v1/empresas/

# 4. Verificar VITE_API_URL en .env.production
cat .env.production

# 5. Rebuild del frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run build

# 6. Subir nuevamente
scp -r dist/* u123456789@tu-dominio.com:public_html/
```

### Error de CORS

#### Síntomas
- Error en consola: "Access to fetch at '...' from origin '...' has been blocked by CORS policy"

#### Solución

En backend `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
    "http://localhost:5173",  # Solo desarrollo
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### Imágenes no se Cargan

#### Síntomas
- Iconos de empresas/productos no muestran

#### Solución

```bash
# 1. Verificar permisos de carpeta media
chmod -R 755 public_html/media
chown -R u123456789:u123456789 public_html/media

# 2. Verificar MEDIA_ROOT en settings.py
python manage.py shell
>>> from django.conf import settings
>>> print(settings.MEDIA_ROOT)
>>> print(settings.MEDIA_URL)

# 3. Verificar que archivos existen
ls -la public_html/media/

# 4. Agregar configuración en .htaccess
<Directory "/home/u123456789/public_html/media">
    Require all granted
</Directory>
```

### Build de Frontend Falla

#### Síntomas
- Error durante `npm run build`

#### Solución

```bash
# 1. Limpiar node_modules
rm -rf node_modules package-lock.json

# 2. Limpiar caché de npm
npm cache clean --force

# 3. Reinstalar
npm install

# 4. Verificar versión de Node
node --version  # Debe ser 18+
npm --version

# 5. Actualizar Node (si es necesario)
nvm install 18
nvm use 18

# 6. Intentar build nuevamente
npm run build
```

### Service Worker no se Registra

#### Síntomas
- PWA no funciona offline
- Service Worker no aparece en DevTools

#### Solución

```javascript
// 1. Verificar que sw.js esté en public/
ls -la frontend/public/sw.js

// 2. Verificar registro en main.js
navigator.serviceWorker.register('/sw.js')

// 3. Verificar HTTPS (requerido para SW)
// SSL debe estar instalado

// 4. Limpiar caché del navegador
// F12 → Application → Clear storage

// 5. Forzar registro
navigator.serviceWorker.register('/sw.js', { scope: '/' })
  .then(reg => console.log('SW registrado:', reg))
  .catch(err => console.error('Error SW:', err))
```

### Redis no Conecta

#### Síntomas
- Error "Connection refused"
- Caché no funciona

#### Solución

```bash
# 1. Verificar servicio Redis
redis-cli ping
# Debe responder: PONG

# 2. Reiniciar servicio
sudo systemctl restart redis

# 3. Verificar configuración
redis-cli CONFIG GET bind

# 4. En Hostinger, Redis puede no estar disponible
# Deshabilitar caché Redis en settings.py:

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### Error 404 en Rutas del Frontend

#### Síntomas
- Al recargar página en ruta `/empresa/x`, da 404

#### Solución

Verificar `.htaccess` en `/public_html/`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_URI} !^/backend/
  RewriteCond %{REQUEST_URI} !^/api/
  RewriteCond %{REQUEST_URI} !^/admin/
  RewriteCond %{REQUEST_URI} !^/static/
  RewriteCond %{REQUEST_URI} !^/media/
  RewriteRule . /index.html [L]
</IfModule>
```

---

## 📊 Métricas de Éxito

### KPIs Principales

#### Rendimiento

| Métrica | Objetivo | Cómo Medir |
|---------|----------|------------|
| Primer render | < 2 segundos | Chrome DevTools → Lighthouse |
| Bundle inicial | < 300 KB | `npm run build` → analizar dist/ |
| Tiempo de respuesta API | < 200ms | Chrome DevTools → Network |
| Puntuación Lighthouse | > 90 | Chrome DevTools → Lighthouse |

#### Uso

| Métrica | Objetivo (1er mes) | Cómo Medir |
|---------|-------------------|------------|
| Empresas registradas | 50+ | Admin Django → Businesses |
| Productos activos | 500+ | Admin Django → Products |
| Clicks WhatsApp/día | 100+ | `SELECT COUNT(*) FROM analytics_clickwhatsapp WHERE fecha >= NOW() - INTERVAL 1 DAY` |
| Tasa conversión (vista → click) | 15-25% | `clicks / vistas * 100` |
| Visitas diarias | 1000+ | Google Analytics |

#### Técnico

| Métrica | Objetivo | Cómo Medir |
|---------|----------|------------|
| Uptime | > 99% | Uptime Robot |
| Errores 5xx | < 0.1% | Logs de Hostinger |
| Consumo datos por sesión | < 1MB | Chrome DevTools → Network |

### Monitoreo

#### Desde Django Shell

```bash
cd /workspace/backend
source venv/bin/activate
python manage.py shell
```

```python
from analytics.models import ClickWhatsApp, VistaEmpresa
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

# Clicks últimos 7 días
desde = timezone.now() - timedelta(days=7)
clicks_7d = ClickWhatsApp.objects.filter(fecha__gte=desde).count()
print(f'Clicks últimos 7 días: {clicks_7d}')

# Clicks por empresa (top 10)
from django.db.models import Count
top_empresas = ClickWhatsApp.objects.values(
    'empresa__nombre'
).annotate(total=Count('id')).order_by('-total')[:10]

for emp in top_empresas:
    print(f"{emp['empresa__nombre']}: {emp['total']} clicks")

# Tasa de conversión
vistas = VistaEmpresa.objects.filter(fecha__gte=desde).count()
tasa = (clicks_7d / vistas * 100) if vistas > 0 else 0
print(f'Tasa de conversión: {tasa:.2f}%')
```

#### Herramientas Recomendadas

1. **Google Analytics** - Tráfico y comportamiento
2. **Google Search Console** - SEO y errores de rastreo
3. **Uptime Robot** - Monitoreo de disponibilidad (gratis)
4. **Sentry** - Tracking de errores (plan gratis disponible)
5. **Chrome DevTools** - Performance y debugging

---

## ✅ Checklist de Despliegue

### Despliegue Local

- [ ] Python 3.9+ instalado
- [ ] Node.js 18+ instalado
- [ ] MySQL/MariaDB instalado y corriendo
- [ ] Redis instalado y corriendo (opcional)
- [ ] Backend dependencies instaladas
- [ ] Base de datos creada
- [ ] Archivo `.env` configurado
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Frontend dependencies instaladas
- [ ] Archivo `.env` frontend configurado
- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Frontend corriendo en `http://localhost:5173`
- [ ] Health check responde
- [ ] Botón WhatsApp funciona
- [ ] Service Worker registrado

### Despliegue Hostinger

- [ ] Plan Business o superior contratado
- [ ] SSH habilitado en hPanel
- [ ] Base de datos creada en hPanel
- [ ] Credenciales de BD guardadas
- [ ] Backend subido vía FTP a `/public_html/backend/`
- [ ] Aplicación Python creada en hPanel
- [ ] passenger_wsgi.py configurado con ruta correcta
- [ ] Dependencias instaladas vía SSH
- [ ] Variables de entorno configuradas en .htaccess
- [ ] Migraciones aplicadas en producción
- [ ] Archivos estáticos recopilados
- [ ] Superusuario creado
- [ ] DNS del dominio configurado
- [ ] Dominio apuntado en Hostinger
- [ ] Frontend build generado (`npm run build`)
- [ ] Frontend subido a `/public_html/`
- [ ] .htaccess configurado para SPA
- [ ] SSL instalado (Let's Encrypt)
- [ ] HTTPS forzado
- [ ] Health check responde en producción
- [ ] Botón WhatsApp funciona en producción
- [ ] Analytics de clicks funcionando

### Post-Despliegue

- [ ] Backup automático configurado
- [ ] Monitoreo de uptime activado
- [ ] Google Analytics instalado
- [ ] Google Search Console configurado
- [ ] Pruebas en móvil realizadas
- [ ] Pruebas offline realizadas
- [ ] Documentación actualizada
- [ ] Equipo capacitado

---

## 📞 Soporte y Recursos

### Documentación Oficial

- **Django:** https://docs.djangoproject.com/es/4.2/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Vue 3:** https://vuejs.org/
- **Pinia:** https://pinia.vuejs.org/
- **Tailwind CSS:** https://tailwindcss.com/
- **Vite:** https://vitejs.dev/
- **Hostinger:** https://www.hostinger.com/tutorials

### Comunidades

- **Django España:** https://discord.gg/django-espana
- **Vue.js Latinoamérica:** https://t.me/vuejs_latam
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/django+vue.js

### Contacto Hostinger

- **Soporte 24/7:** Chat en vivo en hPanel
- **Base de conocimientos:** https://www.hostinger.com/tutorials
- **Estado del servicio:** https://status.hostinger.com/

---

## 📄 Licencia

Este proyecto es propiedad intelectual de Tu Merkadito.

---

## 📝 Notas Finales

### Optimizaciones Específicas para Cuba

1. **Bundle < 300KB:** Usar code splitting y lazy loading
2. **Imágenes WebP:** Convertir automáticamente al subir
3. **Paginación obligatoria:** Máximo 20 items por página
4. **Caché agresivo:** Service workers + IndexedDB
5. **Offline first:** Toda la app funciona sin internet
6. **WhatsApp centric:** Todo termina en WhatsApp
7. **Geolocalización ligera:** Sin Google Maps, usar OpenStreetMap

### Próximos Pasos (Fases Futuras)

- **Fase 6:** Analíticas Ligeras (Dashboard básico)
- **Fase 7:** Tu Merkadito Business (Panel para negocios)
- **Fase 8:** Tu Merkadito POS (Punto de venta independiente)

---

**Última actualización:** Junio 2025  
**Versión:** 1.5.0 (Fases 0-5 Completadas)  
**Estado:** ✅ Producción Ready  
**Documentación completa:** Sí
