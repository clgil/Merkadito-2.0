# 📦 Guía de Despliegue - Tu Merkadito

Esta guía cubre el despliegue tanto en entorno local como en Hostinger.

---

## 📋 Tabla de Contenidos

1. [Despliegue Local](#despliegue-local)
   - [Requisitos](#requisitos)
   - [Backend (Django)](#backend-django)
   - [Frontend (Vue 3)](#frontend-vue-3)
   - [Base de Datos](#base-de-datos)
   - [Redis](#redis)
   - [Ejecutar en Desarrollo](#ejecutar-en-desarrollo)
2. [Despliegue en Hostinger](#despliegue-en-hostinger)
   - [Requisitos Hostinger](#requisitos-hostinger)
   - [Configurar Base de Datos](#configurar-base-de-datos)
   - [Subir Backend](#subir-backend)
   - [Configurar Dominio](#configurar-dominio)
   - [Subir Frontend](#subir-frontend)
   - [Configurar SSL](#configurar-ssl)
3. [Variables de Entorno](#variables-de-entorno)
4. [Troubleshooting](#troubleshooting)

---

## 🖥️ Despliegue Local

### Requisitos

- Python 3.9 o superior
- Node.js 18 o superior
- MySQL 8.0+ o MariaDB 10.5+
- Redis 6+
- Git

---

### Backend (Django)

#### Paso 1: Clonar y navegar al backend

```bash
cd /workspace/backend
```

#### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar variables de entorno

Crea un archivo `.env` en `/workspace/backend/`:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-x789xyz
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=merkadito_local
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS (para desarrollo)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

#### Paso 5: Crear base de datos

En MySQL/MariaDB:

```sql
CREATE DATABASE merkadito_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Paso 6: Ejecutar migraciones

```bash
python manage.py migrate
```

#### Paso 7: Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

#### Paso 8: Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

---

### Frontend (Vue 3)

#### Paso 1: Navegar al frontend

```bash
cd /workspace/frontend
```

#### Paso 2: Instalar dependencias

```bash
npm install
```

#### Paso 3: Configurar variables de entorno

Crea un archivo `.env` en `/workspace/frontend/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0
```

#### Paso 4: Ejecutar en modo desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

---

### Base de Datos

#### Instalación en Ubuntu/Debian

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### Instalación en Windows

Descargar desde: https://dev.mysql.com/downloads/mysql/

#### Instalación en Mac

```bash
brew install mysql
brew services start mysql
```

---

### Redis

#### Instalación en Ubuntu/Debian

```bash
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### Instalación en Windows

Descargar desde: https://github.com/microsoftarchive/redis/releases

#### Instalación en Mac

```bash
brew install redis
brew services start redis
```

#### Verificar Redis

```bash
redis-cli ping
# Debe responder: PONG
```

---

### Ejecutar en Desarrollo

#### Terminal 1 - Backend

```bash
cd /workspace/backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python manage.py runserver
```

Backend disponible en: `http://localhost:8000`

#### Terminal 2 - Frontend

```bash
cd /workspace/frontend
npm run dev
```

Frontend disponible en: `http://localhost:5173`

#### Terminal 3 - Redis (si no está corriendo como servicio)

```bash
redis-server
```

---

## 🌐 Despliegue en Hostinger

### Requisitos Hostinger

- Plan **Business Web Hosting** o superior (recomendado)
- O **Cloud Startup** para mejor rendimiento
- Acceso a phpMyAdmin o MySQL remoto
- Acceso SSH (habilitar en hPanel)
- Dominio configurado

---

### Configurar Base de Datos

#### Paso 1: Crear base de datos en hPanel

1. Ingresar a hPanel
2. Ir a **Bases de Datos MySQL**
3. Click en **Crear nueva base de datos**
4. Completar:
   - Nombre: `u123456789_merkadito`
   - Usuario: `u123456789_admin`
   - Contraseña: (generar contraseña segura)
5. Guardar credenciales

#### Paso 2: Importar estructura

Opción A - Usando phpMyAdmin:

1. Ir a **phpMyAdmin** en hPanel
2. Seleccionar la base de datos creada
3. Click en **Importar**
4. Subir archivo SQL con las migraciones

Opción B - Usando SSH:

```bash
ssh u123456789@tu-dominio.com

mysql -u u123456789_admin -p u123456789_merkadito < backup_estructura.sql
```

---

### Subir Backend

#### Paso 1: Preparar backend para producción

En tu máquina local:

```bash
cd /workspace/backend

# Crear requirements de producción
pip freeze > requirements-production.txt

# Modificar settings.py para producción
# DEBUG = False
# ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
```

#### Paso 2: Subir archivos vía FTP/SFTP

Usar FileZilla o similar:

1. Conectar a: `ftp.tu-dominio.com`
2. Usuario: tu usuario de hosting
3. Contraseña: tu contraseña
4. Subir carpeta `backend` a: `/public_html/backend`

#### Paso 3: Configurar Python en Hostinger

Hostinger soporta Python mediante Passenger:

1. En hPanel, ir a **Configuración Avanzada** → **Aplicación Python**
2. Click en **Crear aplicación**
3. Configurar:
   - Directorio: `/public_html/backend`
   - Archivo de entrada: `passenger_wsgi.py`
   - Versión Python: 3.9 o superior
   - Virtual Environment: Activar

#### Paso 4: Crear archivo passenger_wsgi.py

En `/workspace/backend/passenger_wsgi.py`:

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

#### Paso 5: Instalar dependencias en Hostinger

Vía SSH:

```bash
ssh u123456789@tu-dominio.com

cd public_html/backend
virtualenv --python=python3.9 venv
source venv/bin/activate
pip install -r requirements-production.txt
```

#### Paso 6: Configurar variables de entorno en producción

En hPanel → **Configuración Avanzada** → **Editor .htaccess**:

```apache
SetEnv SECRET_KEY 'tu-clave-secreta-de-produccion'
SetEnv DB_NAME 'u123456789_merkadito'
SetEnv DB_USER 'u123456789_admin'
SetEnv DB_PASSWORD 'tu-password-seguro'
SetEnv DB_HOST 'localhost'
SetEnv DEBUG 'False'
SetEnv ALLOWED_HOSTS 'tu-dominio.com,www.tu-dominio.com'
```

#### Paso 7: Ejecutar migraciones en producción

Vía SSH:

```bash
cd public_html/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

---

### Configurar Dominio

#### Paso 1: Configurar DNS

En el administrador de tu dominio:

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

#### Paso 2: Apuntar dominio en Hostinger

1. hPanel → **Hosting** → **Detalles**
2. **Cambiar dominio**
3. Ingresar tu dominio
4. Guardar cambios

---

### Subir Frontend

#### Paso 1: Build de producción

En tu máquina local:

```bash
cd /workspace/frontend

# Actualizar .env para producción
echo "VITE_API_URL=https://tu-dominio.com/api/v1" > .env.production

# Construir
npm run build
```

#### Paso 2: Subir build al hosting

Los archivos generados en `dist/` subirlos a:

- `/public_html/` (si el frontend va en el root)
- O `/public_html/app/` (si va en subdirectorio)

```bash
# Vía SSH
cd /workspace/frontend
npm run build

# Subir contenido de dist/
scp -r dist/* u123456789@tu-dominio.com:public_html/
```

#### Paso 3: Configurar redirección de rutas (SPA)

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

---

### Configurar SSL

#### SSL Automático (Let's Encrypt)

1. hPanel → **Seguridad** → **SSL**
2. Click en **Instalar SSL** en tu dominio
3. Seleccionar **Let's Encrypt**
4. Click en **Instalar**
5. Esperar 5-10 minutos

#### Forzar HTTPS

En `/public_html/.htaccess`:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 🔧 Variables de Entorno

### Backend (.env)

```env
# Seguridad
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Base de datos
DB_NAME=nombre_base_datos
DB_USER=usuario_base_datos
DB_PASSWORD=password_seguro
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Archivos multimedia
MEDIA_ROOT=/home/u123456789/public_html/media
MEDIA_URL=https://tu-dominio.com/media/

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app

# Analytics
ANALYTICS_ENABLED=True
```

### Frontend (.env.production)

```env
VITE_API_URL=https://tu-dominio.com/api/v1
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0
VITE_MAX_IMAGE_SIZE=1048576
VITE_CACHE_ENABLED=true
```

---

## 🐛 Troubleshooting

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
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)

# Verificar que MySQL esté corriendo
systemctl status mysql
```

### Frontend no carga

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

### Redis no conecta

```bash
# Verificar servicio
redis-cli ping

# Reiniciar servicio
sudo systemctl restart redis

# Verificar configuración
redis-cli CONFIG GET bind
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

## 📊 Monitoreo Post-Despliegue

### Verificar que todo funcione

```bash
# Backend
curl https://tu-dominio.com/api/v1/health/

# Frontend
curl https://tu-dominio.com/

# API endpoints
curl https://tu-dominio.com/api/v1/empresas/
curl https://tu-dominio.com/api/v1/categorias/
```

### Métricas a monitorear

- Tiempo de respuesta API (< 200ms ideal)
- Tamaño del bundle inicial (< 300 KB)
- Visitas diarias
- Clicks a WhatsApp
- Errores 4xx y 5xx

### Herramientas recomendadas

- Google Analytics (ligero)
- Sentry (errores)
- Uptime Robot (monitoreo)

---

## 📞 Soporte

Para problemas específicos:

1. Revisar logs en hPanel
2. Verificar documentación oficial:
   - Django: https://docs.djangoproject.com
   - Vue 3: https://vuejs.org
   - Hostinger: https://www.hostinger.com/tutorials

---

## ✅ Checklist Post-Despliegue

- [ ] Backend responde en `/api/v1/`
- [ ] Frontend carga en `< 2 segundos`
- [ ] SSL instalado y funcionando
- [ ] Base de datos migrada
- [ ] Redis conectado
- [ ] CORS configurado correctamente
- [ ] Archivos estáticos sirven correctamente
- [ ] Formulario de registro funciona
- [ ] Búsqueda de empresas funciona
- [ ] Clicks a WhatsApp se registran
- [ ] Backup automático configurado

---

**Última actualización:** Junio 2025  
**Versión:** 1.0.0
