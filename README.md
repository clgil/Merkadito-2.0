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
- [📘 Guía Completa de Despliegue](#-guía-completa-de-despliegue)
- [Documentación por Fase](#documentación-por-fase)

---

## 🎯 Estado del Proyecto

### ✅ Fases 0-5 COMPLETADAS Y EN PRODUCCIÓN

La **Fase 5 - Sistema WhatsApp Centric** está **completamente implementada** y lista para producción.

**Características principales:**
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
| **Fase 1** | Nuevo Diseño UI | ✅ Completada | Tailwind, Shadcn Vue |
| **Fase 2** | PWA Offline | ✅ Completada | `FASE_2_IMPLEMENTADA.md`, `PRD_FASE_2_PWA.md` |
| **Fase 3** | Marketplace Ultraligero | ✅ Completada | `FASE_3_IMPLEMENTADA.md` |
| **Fase 4** | Geolocalización Cubana | ✅ Completada | `FASE_4_GEOLOCALIZACION_IMPLEMENTADA.md` |
| **Fase 5** | Sistema WhatsApp Centric | ✅ **COMPLETADA** | `FASE_5_WHATSAPP_CENTRIC.md` |

### Próximas Fases

| Fase | Descripción | Duración | Estado |
|------|-------------|----------|--------|
| **Fase 6** | Analíticas Ligeras | 2 semanas | Pendiente |
| **Fase 7** | Tu Merkadito Business | 4 semanas | Pendiente |
| **Fase 8** | Tu Merkadito POS | 8-12 semanas | Pendiente |

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

## 📘 Guía Completa de Despliegue

** Toda la información necesaria para desplegar tanto localmente como en Hostinger está en:**

👉 **`GUIA_COMPLETA_DESPLEGUE.md`** 👈

Esta guía incluye:

### Despliegue Local
- Requisitos previos (Python, Node.js, MySQL, Redis)
- Configuración paso a paso del backend
- Configuración paso a paso del frontend
- Ejecución en modo desarrollo
- Verificación de instalación

### Despliegue en Hostinger
- Requisitos del plan de hosting
- Configuración de base de datos en hPanel
- Subida de archivos vía FTP/SFTP
- Configuración de Python en Hostinger
- Instalación de dependencias vía SSH
- Variables de entorno en producción
- Configuración de dominio y DNS
- Build y subida del frontend
- Instalación de SSL (Let's Encrypt)
- Redirección SPA para Vue Router

### Troubleshooting
- Error 500 en backend
- Error de conexión a base de datos
- Clicks a WhatsApp no se registran
- Frontend no carga
- Errores de CORS
- Imágenes no se cargan
- Build de frontend falla
- Service Worker no se registra
- Y más...

### Métricas de Éxito
- KPIs de rendimiento (< 2s render, < 300KB bundle)
- KPIs de uso (empresas, productos, clicks WhatsApp)
- KPIs técnicos (uptime, errores)
- Scripts de monitoreo desde Django Shell

---

## 📚 Documentación por Fase

| Documento | Descripción |
|-----------|-------------|
| **`GUIA_COMPLETA_DESPLEGUE.md`** | 📘 **GUÍA PRINCIPAL** - Todo lo necesario para desplegar local y en Hostinger |
| `FASE_5_WHATSAPP_CENTRIC.md` | Detalles de implementación Fase 5 + despliegue |
| `DEPLOYMENT.md` | Guía alternativa de despliegue |
| `PRD_FASE_INICIAL.md` | PRD inicial y arquitectura del proyecto |
| `FASE_2_IMPLEMENTADA.md` | Detalles de implementación PWA Offline |
| `PRD_FASE_2_PWA.md` | PRD de la Fase 2 PWA |
| `FASE_3_IMPLEMENTADA.md` | Detalles de Marketplace Ultraligero |
| `FASE_3_MARKETPLACE_ULTRALIGERO.md` | PRD de la Fase 3 |
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

📖 **Más soluciones:** Ver sección "Troubleshooting" en `GUIA_COMPLETA_DESPLEGUE.md`

---

## 📈 Métricas de Éxito

- ✅ Primer render < 2 segundos
- ✅ Bundle inicial < 300 KB
- ✅ Funcionamiento offline completo
- ✅ Clicks a WhatsApp como métrica principal
- ✅ Consumo de datos < 1MB por sesión

---

## 🎯 Próximos Pasos

Según el PRD analizado, las próximas fases son:

1. **Fase 6** - Analíticas Ligeras (Dashboard básico para negocios)
2. **Fase 7** - Tu Merkadito Business (Panel privado para negocios)
3. **Fase 8** - Tu Merkadito POS (Producto independiente de punto de venta)

**Nota:** El PRD recomienda implementar estas fases de manera incremental, solo cuando se tenga masa crítica de usuarios y negocios en la plataforma.

---

## 📞 Soporte

Para problemas específicos:
1. Revisar logs en hPanel
2. Consultar `GUIA_COMPLETA_DESPLEGUE.md`
3. Verificar documentación oficial:
   - Django: https://docs.djangoproject.com
   - Vue 3: https://vuejs.org
   - DRF: https://www.django-rest-framework.org
   - Hostinger: https://www.hostinger.com/tutorials

---

**Última actualización:** Junio 2025  
**Versión:** 1.5.0 (Fases 0-5 Completadas)  
**Estado:** ✅ Producción Ready  
**Guía de despliegue:** `GUIA_COMPLETA_DESPLEGUE.md`
