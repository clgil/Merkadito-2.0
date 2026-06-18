# Frontend - Tu Merkadito

Aplicación Vue 3 ultraligera para Tu Merkadito.

## Stack Tecnológico

- **Vue 3** (Composition API)
- **Vite** (Build tool rápido)
- **Pinia** (Gestión de estado)
- **Vue Router** (Rutas)
- **Tailwind CSS** (Estilos)
- **PWA** (Service Workers + IndexedDB)

## Estructura

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── .env
├── public/
│   ├── manifest.json
│   └── sw.js
└── src/
    ├── main.js
    ├── App.vue
    ├── router/
    │   └── index.js
    ├── stores/
    │   ├── businesses.js
    │   ├── products.js
    │   └── favorites.js
    ├── views/
    │   ├── Home.vue
    │   ├── Search.vue
    │   ├── BusinessDetail.vue
    │   └── BusinessPanel.vue
    ├── components/
    │   ├── Header.vue
    │   ├── Footer.vue
    │   ├── BusinessCard.vue
    │   ├── ProductCard.vue
    │   └── SearchBar.vue
    ├── utils/
    │   ├── api.js
    │   └── offline.js
    └── assets/
        └── styles.css
```

## Instalación

```bash
cd frontend
npm install
```

## Configuración

Crear archivo `.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME="Tu Merkadito"
VITE_APP_VERSION=1.0.0
```

## Desarrollo

```bash
npm run dev
```

Disponible en: `http://localhost:5173`

## Build Producción

```bash
npm run build
```

Los archivos se generan en `dist/`

## Optimizaciones para Cuba

- Bundle inicial < 300 KB
- Lazy loading de rutas
- Service Workers para offline
- IndexedDB para caché local
- Imágenes WebP optimizadas
- Sin dependencias pesadas
