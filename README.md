# 🏪 Tu Merkadito - Directorio Comercial Ultraligero para Cuba

**El directorio comercial y catálogo de productos más rápido de Cuba conectado a WhatsApp.**

Tu Merkadito está optimizado para la realidad cubana:
- ✅ Internet lento e inestable
- ✅ Datos móviles limitados
- ✅ Equipos antiguos y móviles de gama baja
- ✅ Apagones frecuentes
- ✅ Funcionamiento offline completo

---

## 📋 Tabla de Contenidos

- [Estado del Proyecto](#estado-del-proyecto)
- [Fases Implementadas](#fases-implementadas)
- [Arquitectura](#arquitectura)
- [Despliegue Local](#despliegue-local)
- [Despliegue en Hostinger](#despliegue-en-hostinger)
- [Documentación Completa](#documentación-completa)

---

## 🎯 Estado del Proyecto

### ✅ Fase 5 - Sistema WhatsApp Centric (IMPLEMENTADA)

La Fase 5 está **completamente implementada** y lista para producción.

**Características:**
- Botones 📲 WhatsApp en todas las empresas y productos
- Registro automático de clicks a WhatsApp
- Analítica ligera de vistas y clicks
- Sincronización offline de acciones
- Estadísticas básicas por empresa

**Endpoints API:**
```
POST /api/v1/analytics/click/           # Registrar click a WhatsApp
POST /api/v1/analytics/vista-empresa/   # Registrar vista a empresa
POST /api/v1/analytics/vista-producto/  # Registrar vista a producto
GET  /api/v1/analytics/estadisticas/<id>/ # Obtener estadísticas
```

---

## 📁 Fases Implementadas

| Fase | Descripción | Estado | Documento |
|------|-------------|--------|-----------|
| **Fase 0** | Optimización del Core | ✅ Completada | `PRD_FASE_INICIAL.md` |
| **Fase 2** | PWA Offline | ✅ Completada | `FASE_2_IMPLEMENTADA.md`, `PRD_FASE_2_PWA.md` |
| **Fase 3** | Marketplace Ultraligero | ✅ Completada | `FASE_3_IMPLEMENTADA.md`, `FASE_3_MARKETPLACE_ULTRALIGERO.md` |
| **Fase 4** | Geolocalización Cubana | ✅ Completada | `FASE_4_GEOLOCALIZACION_IMPLEMENTADA.md` |
| **Fase 5** | Sistema WhatsApp Centric | ✅ **COMPLETADA** | `FASE_5_WHATSAPP_CENTRIC.md` |

---

## 🏗️ Arquitectura

### Backend
- **Framework:** Django 4.x + Django REST Framework
- **Base de Datos:** MySQL 8.0+ / MariaDB 10.5+
- **Caché:** Redis 6+
- **Modelos:** Empresas, Productos, Analytics (ClickWhatsApp, VistaEmpresa, VistaProducto)

### Frontend
- **Framework:** Vue 3 (Vite)
- **Estado:** Pinia
- **Router:** Vue Router
- **Estilos:** Tailwind CSS
- **PWA:** Service Workers + IndexedDB

---

## 🚀 Despliegue Local

### Requisitos Previos
- Python 3.9+
- Node.js 18+
- MySQL 8.0+ o MariaDB 10.5+
- Redis 6+ (opcional)

### Pasos Rápidos

```bash
# 1. Backend
cd /workspace/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env (ver FASE_5_WHATSAPP_CENTRIC.md)
python manage.py migrate
python manage.py runserver

# 2. Frontend (otra terminal)
cd /workspace/frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
npm run dev
```

**Acceso:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/v1/
- Admin Django: http://localhost:8000/admin/

📖 **Guía completa:** Ver sección "Despliegue Local" en `FASE_5_WHATSAPP_CENTRIC.md`

---

## 🌐 Despliegue en Hostinger

### Requisitos
- Plan Business Web Hosting o superior
- Acceso SSH habilitado
- Dominio configurado

### Pasos Resumen

1. **Configurar BD** en hPanel → Bases de Datos MySQL
2. **Subir backend** vía FTP a `/public_html/backend`
3. **Configurar Python** en hPanel → Aplicación Python
4. **Instalar dependencias** vía SSH
5. **Ejecutar migraciones:** `python manage.py migrate`
6. **Build frontend:** `npm run build` y subir `dist/` a `/public_html/`
7. **Configurar SSL** con Let's Encrypt

📖 **Guía completa:** Ver sección "Despliegue en Hostinger" en `FASE_5_WHATSAPP_CENTRIC.md`

---

## 📊 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| `FASE_5_WHATSAPP_CENTRIC.md` | 📘 **Guía principal** - Implementación Fase 5 + despliegue completo |
| `DEPLOYMENT.md` | Guía detallada de despliegue local y Hostinger |
| `PRD_FASE_INICIAL.md` | PRD inicial y arquitectura del proyecto |
| `FASE_2_IMPLEMENTADA.md` | Detalles de implementación PWA Offline |
| `FASE_3_IMPLEMENTADA.md` | Detalles de Marketplace Ultraligero |
| `FASE_4_GEOLOCALIZACION_IMPLEMENTADA.md` | Detalles de Geolocalización Cubana |

---

## 🔧 Troubleshooting Rápido

### Error 500 en Backend
```bash
tail -f /home/u123456789/logs/errors.log
chmod -R 755 public_html/backend
```

### CORS Error
Agregar en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = ["https://tu-dominio.com"]
```

### Frontend no carga
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run build
```

📖 **Más soluciones:** Ver sección "Troubleshooting" en `FASE_5_WHATSAPP_CENTRIC.md`

---

## 📈 Métricas de Éxito

- ✅ Primer render < 2 segundos
- ✅ Bundle inicial < 300 KB
- ✅ Funcionamiento offline completo
- ✅ Clicks a WhatsApp como métrica principal
- ✅ Consumo de datos < 1MB por sesión

---

## 🎯 Próximas Fases

| Fase | Descripción | Duración Estimada |
|------|-------------|-------------------|
| **Fase 6** | Analíticas Ligeras | 2 semanas |
| **Fase 7** | Tu Merkadito Business | 4 semanas |
| **Fase 8** | Tu Merkadito POS | 8-12 semanas |

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

**Última actualización:** Junio 2025  
**Versión:** 1.5.0 (Fase 5 Completada)  
**Estado:** ✅ Producción Ready
