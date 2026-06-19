# Tu Merkadito Frontend - PWA Offline

Aplicación Vue 3 con soporte PWA completo para funcionar offline.

## Características

- ✅ Service Workers para caché agresivo
- ✅ IndexedDB para almacenamiento local
- ✅ Sincronización automática cuando hay conexión
- ✅ Funcionamiento completo sin internet
- ✅ Optimizado para conexiones lentas (Cuba)

## Instalación

```bash
cd /workspace/frontend

# Instalar dependencias
npm install

# Copiar variables de entorno
cp .env.example .env

# Iniciar servidor de desarrollo
npm run dev
```

## Build para producción

```bash
npm run build
```

Los archivos generados estarán en `dist/`.

## Estructura del Proyecto

```
frontend/
├── public/
│   ├── manifest.json      # Manifiesto PWA
│   ├── sw.js              # Service Worker
│   └── favicon.svg
├── src/
│   ├── assets/            # CSS y assets globales
│   ├── components/        # Componentes reutilizables
│   ├── pwa/               # Lógica PWA (db, sync, cache)
│   ├── router/            # Configuración de rutas
│   ├── stores/            # Stores Pinia (offline, favoritos)
│   ├── views/             # Vistas principales
│   ├── App.vue            # Componente raíz
│   └── main.js            # Punto de entrada
├── index.html
├── package.json
├── vite.config.js         # Configuración Vite + PWA
├── tailwind.config.js     # Configuración Tailwind
└── postcss.config.js
```

## Pruebas Offline

1. Abrir Chrome DevTools (F12)
2. Ir a Application > Service Workers
3. En Network panel, seleccionar "Offline"
4. Recargar la página

La aplicación seguirá funcionando con datos en caché.

## Métricas de Rendimiento

- Primera carga: < 2 segundos
- Cargas subsiguientes: < 0.5 segundos
- Bundle inicial: < 300 KB
- Consumo de datos: < 500 KB por sesión

## Tecnologías

- Vue 3 (Composition API)
- Vite
- Pinia
- Vue Router
- Tailwind CSS
- Workbox (PWA)
- IndexedDB (idb)
