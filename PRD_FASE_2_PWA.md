# Tu Merkadito - Fase 2: PWA Offline

## Descripción

Implementación completa de Progressive Web App (PWA) con funcionalidad offline total, optimizada para las condiciones de Cuba:

- ✅ Service Workers para caché agresivo
- ✅ IndexedDB para almacenamiento local
- ✅ Estrategia Cache First
- ✅ Sincronización automática cuando hay conexión
- ✅ Funcionamiento completo sin internet

---

## Arquitectura PWA

### Service Worker

Estrategias de caché implementadas:

1. **Cache First**: Para assets estáticos (CSS, JS, imágenes)
2. **Network First**: Para datos dinámicos (empresas, productos)
3. **Stale While Revalidate**: Para contenido que puede estar desactualizado

### IndexedDB

Almacenamiento local para:

- Empresas visitadas
- Productos vistos
- Búsquedas recientes
- Favoritos del usuario
- Datos de sesión

### Sincronización

Cuando se restablece la conexión:

1. Verificar cambios locales
2. Enviar datos pendientes al servidor
3. Actualizar caché con datos frescos
4. Notificar al usuario

---

## Estructura de Archivos

```
frontend/
├── public/
│   ├── sw.js                 # Service Worker principal
│   └── manifest.json         # Manifiesto PWA
├── src/
│   ├── pwa/
│   │   ├── db.js             # Configuración IndexedDB
│   │   ├── sync.js           # Lógica de sincronización
│   │   └── cache.js          # Utilidades de caché
│   ├── stores/
│   │   ├── offline.js        # Store Pinia para estado offline
│   │   └── favorites.js      # Store para favoritos
│   └── components/
│       └── OfflineBanner.vue # Banner de estado de conexión
```

---

## Instalación

### 1. Instalar dependencias adicionales

```bash
cd /workspace/frontend
npm install workbox-build workbox-window vite-plugin-pwa
```

### 2. Configurar Vite PWA

Actualizar `vite.config.js`:

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'Tu Merkadito',
        short_name: 'Merkadito',
        description: 'Directorio comercial de Cuba',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: '/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.tumerkadito\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 // 24 horas
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 días
              }
            }
          }
        ]
      }
    })
  ]
})
```

---

## Implementación IndexedDB

### Archivo: `src/pwa/db.js`

```js
import { openDB } from 'idb'

const DB_NAME = 'tu-merkadito-db'
const DB_VERSION = 1

export async function initDB() {
  return await openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      // Store para empresas
      if (!db.objectStoreNames.contains('empresas')) {
        db.createObjectStore('empresas', { keyPath: 'id' })
      }
      
      // Store para productos
      if (!db.objectStoreNames.contains('productos')) {
        db.createObjectStore('productos', { keyPath: 'id' })
      }
      
      // Store para búsquedas recientes
      if (!db.objectStoreNames.contains('busquedas')) {
        const store = db.createObjectStore('busquedas', { 
          keyPath: 'id', 
          autoIncrement: true 
        })
        store.createIndex('termino', 'termino')
        store.createIndex('fecha', 'fecha')
      }
      
      // Store para favoritos
      if (!db.objectStoreNames.contains('favoritos')) {
        db.createObjectStore('favoritos', { keyPath: 'id' })
      }
      
      // Store para cola de sincronización
      if (!db.objectStoreNames.contains('syncQueue')) {
        const store = db.createObjectStore('syncQueue', { 
          keyPath: 'id', 
          autoIncrement: true 
        })
        store.createIndex('tipo', 'tipo')
        store.createIndex('pendiente', 'pendiente')
      }
    }
  })
}

// Operaciones CRUD genéricas
export async function dbGet(storeName, key) {
  const db = await initDB()
  return await db.get(storeName, key)
}

export async function dbGetAll(storeName) {
  const db = await initDB()
  return await db.getAll(storeName)
}

export async function dbPut(storeName, item) {
  const db = await initDB()
  return await db.put(storeName, item)
}

export async function dbDelete(storeName, key) {
  const db = await initDB()
  return await db.delete(storeName, key)
}

export async function dbClear(storeName) {
  const db = await initDB()
  return await db.clear(storeName)
}

// Métodos específicos para empresas
export async function guardarEmpresa(empresa) {
  return await dbPut('empresas', {
    ...empresa,
    _cached_at: Date.now()
  })
}

export async function obtenerEmpresa(id) {
  return await dbGet('empresas', id)
}

export async function obtenerTodasLasEmpresas() {
  return await dbGetAll('empresas')
}

// Métodos específicos para productos
export async function guardarProducto(producto) {
  return await dbPut('productos', {
    ...producto,
    _cached_at: Date.now()
  })
}

export async function obtenerProductosPorEmpresa(empresaId) {
  const db = await initDB()
  const productos = await db.getAll('productos')
  return productos.filter(p => p.empresa_id === empresaId)
}

// Métodos para búsquedas recientes
export async function guardarBusqueda(termino, resultados = []) {
  const db = await initDB()
  return await db.put('busquedas', {
    termino,
    resultados: resultados.length,
    fecha: new Date().toISOString()
  })
}

export async function obtenerBusquedasRecientes(limit = 10) {
  const db = await initDB()
  const busquedas = await db.getAll('busquedas')
  return busquedas
    .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
    .slice(0, limit)
}

// Métodos para favoritos
export async function toggleFavorito(item) {
  const existente = await dbGet('favoritos', item.id)
  if (existente) {
    await dbDelete('favoritos', item.id)
    return false
  } else {
    await dbPut('favoritos', {
      ...item,
      _added_at: Date.now()
    })
    return true
  }
}

export async function obtenerFavoritos() {
  return await dbGetAll('favoritos')
}

export async function esFavorito(id) {
  const item = await dbGet('favoritos', id)
  return !!item
}

// Cola de sincronización
export async function addToSyncQueue(action) {
  const db = await initDB()
  return await db.put('syncQueue', {
    ...action,
    pendiente: true,
    intentos: 0,
    creado_en: Date.now()
  })
}

export async function getPendingSyncActions() {
  const db = await initDB()
  const actions = await db.getAll('syncQueue')
  return actions.filter(a => a.pendiente)
}

export async function markSyncComplete(id) {
  const db = await initDB()
  await db.delete('syncQueue', id)
}
```

---

## Store Pinia para Estado Offline

### Archivo: `src/stores/offline.js`

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useOfflineStore = defineStore('offline', () => {
  // Estado
  const isOnline = ref(navigator.onLine)
  const isSyncing = ref(false)
  const lastSyncTime = ref(null)
  const pendingActions = ref([])

  // Getters
  const offlineMode = computed(() => !isOnline.value)
  const hasPendingSync = computed(() => pendingActions.value.length > 0)

  // Acciones
  function setOnline(status) {
    isOnline.value = status
    if (status) {
      syncPendingActions()
    }
  }

  function addPendingAction(action) {
    pendingActions.value.push(action)
  }

  function removePendingAction(id) {
    pendingActions.value = pendingActions.value.filter(a => a.id !== id)
  }

  function setLastSyncTime(time) {
    lastSyncTime.value = time
  }

  async function syncPendingActions() {
    if (isSyncing.value || !isOnline.value) return
    
    isSyncing.value = true
    
    try {
      // Importar funciones de sincronización
      const { executeSync } = await import('../pwa/sync')
      await executeSync(pendingActions.value)
      pendingActions.value = []
      lastSyncTime.value = new Date().toISOString()
    } catch (error) {
      console.error('Error en sincronización:', error)
    } finally {
      isSyncing.value = false
    }
  }

  // Escuchar eventos de conexión
  if (typeof window !== 'undefined') {
    window.addEventListener('online', () => setOnline(true))
    window.addEventListener('offline', () => setOnline(false))
  }

  return {
    isOnline,
    isSyncing,
    lastSyncTime,
    pendingActions,
    offlineMode,
    hasPendingSync,
    setOnline,
    addPendingAction,
    removePendingAction,
    setLastSyncTime,
    syncPendingActions
  }
})
```

---

## Componente OfflineBanner

### Archivo: `src/components/OfflineBanner.vue`

```vue
<template>
  <transition name="slide-down">
    <div v-if="showBanner" :class="['offline-banner', bannerClass]">
      <div class="banner-content">
        <span class="banner-icon">{{ icon }}</span>
        <span class="banner-text">{{ message }}</span>
      </div>
      <button v-if="canRetry" @click="onRetry" class="retry-btn">
        Reintentar
      </button>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useOfflineStore } from '@/stores/offline'

const props = defineProps({
  customMessage: String
})

const emit = defineEmits(['retry'])

const offlineStore = useOfflineStore()

const showBanner = computed(() => {
  return offlineStore.offlineMode || offlineStore.isSyncing
})

const bannerClass = computed(() => {
  if (offlineStore.isSyncing) return 'syncing'
  if (offlineStore.offlineMode) return 'offline'
  return ''
})

const icon = computed(() => {
  if (offlineStore.isSyncing) return '🔄'
  if (offlineStore.offlineMode) return '📴'
  return '✅'
})

const message = computed(() => {
  if (props.customMessage) return props.customMessage
  if (offlineStore.isSyncing) return 'Sincronizando datos...'
  if (offlineStore.offlineMode) return 'Estás offline. Mostrando datos en caché.'
  return 'Conexión restaurada'
})

const canRetry = computed(() => {
  return offlineStore.offlineMode && offlineStore.hasPendingSync
})

function onRetry() {
  emit('retry')
}
</script>

<style scoped>
.offline-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 9999;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.offline {
  background-color: #fef3c7;
  color: #92400e;
}

.syncing {
  background-color: #dbeafe;
  color: #1e40af;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.retry-btn {
  padding: 0.25rem 0.75rem;
  background-color: rgba(0,0,0,0.1);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background-color: rgba(0,0,0,0.15);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
```

---

## Lógica de Sincronización

### Archivo: `src/pwa/sync.js`

```js
import { getPendingSyncActions, markSyncComplete } from './db'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export async function executeSync(actions) {
  if (!actions || actions.length === 0) return
  
  const results = []
  
  for (const action of actions) {
    try {
      let response
      
      switch (action.tipo) {
        case 'CREATE_EMPRESA':
          response = await axios.post(`${API_BASE_URL}/empresas/`, action.data)
          break
          
        case 'UPDATE_EMPRESA':
          response = await axios.put(
            `${API_BASE_URL}/empresas/${action.data.id}/`, 
            action.data
          )
          break
          
        case 'CREATE_PRODUCTO':
          response = await axios.post(`${API_BASE_URL}/productos/`, action.data)
          break
          
        case 'DELETE_PRODUCTO':
          response = await axios.delete(
            `${API_BASE_URL}/productos/${action.data.id}/`
          )
          break
          
        case 'ANALYTICS_CLICK':
          response = await axios.post(
            `${API_BASE_URL}/analytics/click/`, 
            action.data
          )
          break
          
        default:
          console.warn(`Tipo de acción desconocido: ${action.tipo}`)
          continue
      }
      
      if (response.status >= 200 && response.status < 300) {
        await markSyncComplete(action.id)
        results.push({ success: true, action })
      } else {
        results.push({ success: false, action, error: 'Status no exitoso' })
      }
    } catch (error) {
      console.error('Error sincronizando acción:', action, error)
      
      // Incrementar intentos
      if (action.intentos < 3) {
        action.intentos += 1
      } else {
        // Marcar como fallida después de 3 intentos
        await markSyncComplete(action.id)
      }
      
      results.push({ success: false, action, error: error.message })
    }
  }
  
  return results
}

// Función para sincronizar datos frescos desde el servidor
export async function syncFreshData() {
  try {
    const [empresas, productos] = await Promise.all([
      axios.get(`${API_BASE_URL}/empresas/`),
      axios.get(`${API_BASE_URL}/productos/`)
    ])
    
    // Guardar en caché IndexedDB
    const { guardarEmpresa, guardarProducto } = await import('./db')
    
    for (const empresa of empresas.data.results || empresas.data) {
      await guardarEmpresa(empresa)
    }
    
    for (const producto of productos.data.results || productos.data) {
      await guardarProducto(producto)
    }
    
    return { success: true }
  } catch (error) {
    console.error('Error sincronizando datos frescos:', error)
    return { success: false, error: error.message }
  }
}
```

---

## Service Worker Personalizado

### Archivo: `public/sw.js`

```js
const CACHE_NAME = 'tu-merkadito-v1'
const STATIC_CACHE = 'static-v1'
const DYNAMIC_CACHE = 'dynamic-v1'
const IMAGE_CACHE = 'images-v1'

// Assets estáticos para precaché
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  // Se llenará automáticamente por Vite PWA plugin
]

// Límites de caché
const CACHE_LIMITS = {
  dynamic: 100,
  images: 50
}

// Instalación - Precachear assets estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Precacheando assets estáticos')
      return cache.addAll(STATIC_ASSETS)
    })
  )
  self.skipWaiting()
})

// Activación - Limpiar cachés viejas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && 
                         key !== DYNAMIC_CACHE && 
                         key !== IMAGE_CACHE)
          .map((key) => {
            console.log('[SW] Eliminando caché vieja:', key)
            return caches.delete(key)
          })
      )
    }).then(() => {
      console.log('[SW] Service Worker activado')
      return self.clients.claim()
    })
  )
})

// Fetch - Estrategias de caché
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Ignorar requests de otros orígenes
  if (url.origin !== location.origin) {
    return
  }
  
  // Estrategia para imágenes
  if (request.destination === 'image') {
    event.respondWith(cacheFirst(request, IMAGE_CACHE))
    return
  }
  
  // Estrategia para API
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request, DYNAMIC_CACHE))
    return
  }
  
  // Estrategia para assets estáticos
  event.respondWith(cacheFirst(request, STATIC_CACHE))
})

// Estrategia Cache First
async function cacheFirst(request, cacheName) {
  const cachedResponse = await caches.match(request)
  
  if (cachedResponse) {
    // Actualizar caché en segundo plano
    fetchAndCache(request, cacheName)
    return cachedResponse
  }
  
  return fetchAndCache(request, cacheName)
}

// Estrategia Network First
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request)
    
    // Si la respuesta es exitosa, guardar en caché
    if (networkResponse.ok) {
      const responseClone = networkResponse.clone()
      const cache = await caches.open(cacheName)
      await cache.put(request, responseClone)
    }
    
    return networkResponse
  } catch (error) {
    // Si falla la red, intentar obtener de caché
    const cachedResponse = await caches.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Retornar respuesta offline genérica
    return new Response(
      JSON.stringify({ 
        error: 'offline', 
        message: 'No hay conexión. Mostrando datos en caché.' 
      }),
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
}

// Función auxiliar para fetch y caché
async function fetchAndCache(request, cacheName) {
  try {
    const response = await fetch(request)
    
    if (response.ok) {
      const cache = await caches.open(cacheName)
      const responseClone = response.clone()
      
      // Limitar tamaño del caché
      await trimCache(cacheName, CACHE_LIMITS[cacheName.split('-')[0]] || 100)
      
      await cache.put(request, responseClone)
    }
    
    return response
  } catch (error) {
    console.error('[SW] Error al hacer fetch:', error)
    throw error
  }
}

// Limitar tamaño del caché
async function trimCache(cacheName, maxItems) {
  const cache = await caches.open(cacheName)
  const keys = await cache.keys()
  
  if (keys.length > maxItems) {
    await cache.delete(keys[0])
    await trimCache(cacheName, maxItems)
  }
}

// Mensajes desde el cliente
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    caches.keys().then((keys) => {
      keys.forEach((key) => caches.delete(key))
    })
  }
})
```

---

## Integración en App Principal

### Archivo: `src/main.js`

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { initDB } from './pwa/db'
import { useOfflineStore } from './stores/offline'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Inicializar IndexedDB
initDB().then(() => {
  console.log('[PWA] IndexedDB inicializado')
}).catch((err) => {
  console.error('[PWA] Error inicializando IndexedDB:', err)
})

// Registrar Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('[PWA] SW registrado:', registration.scope)
      })
      .catch((error) => {
        console.error('[PWA] Error registrando SW:', error)
      })
  })
  
  // Escuchar actualizaciones del SW
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.log('[PWA] Nuevo Service Worker activo')
    // Opcional: mostrar notificación de actualización
  })
}

// Inicializar store offline
const offlineStore = useOfflineStore(pinia)
offlineStore.setOnline(navigator.onLine)

app.mount('#app')
```

---

## Comandos de Construcción

### Build para producción

```bash
cd /workspace/frontend

# Instalar dependencias
npm install

# Construir para producción
npm run build

# Vista previa del build
npm run preview
```

### El build generará:

```
dist/
├── index.html
├── manifest.json
├── sw.js              # Service Worker
├── workbox-*.js       # Librerías Workbox
├── assets/
│   ├── index-*.js     # JavaScript con hash
│   ├── index-*.css    # CSS con hash
│   └── *.webp         # Imágenes optimizadas
└── icons/
    ├── icon-192x192.png
    └── icon-512x512.png
```

---

## Pruebas Offline

### 1. Chrome DevTools

1. Abrir DevTools (F12)
2. Ir a Application > Service Workers
3. Verificar que el SW esté activo
4. En Application > Storage, verificar IndexedDB
5. En Network panel, seleccionar "Offline"
6. Recargar la página

### 2. Comandos útiles

```js
// En consola del navegador
// Verificar estado del SW
navigator.serviceWorker.controller

// Ver caché
caches.keys().then(console.log)

// Limpiar todo
caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))

// Forzar actualización
navigator.serviceWorker.ready.then(reg => reg.update())
```

---

## Métricas de Rendimiento

Objetivos para Cuba:

- **Primera carga con internet**: < 2 segundos
- **Cargas subsiguientes (caché)**: < 0.5 segundos
- **Carga offline**: < 1 segundo
- **Consumo de datos**: < 500 KB por sesión
- **Espacio en disco**: < 10 MB máximo

---

## Consideraciones Especiales para Cuba

1. **Apagones frecuentes**: Los datos se guardan inmediatamente en IndexedDB
2. **Internet lento**: Estrategia Cache First reduce solicitudes de red
3. **Equipos antiguos**: Service Worker ligero sin dependencias pesadas
4. **Datos limitados**: Caché agresivo minimiza consumo
5. **Conexiones intermitentes**: Cola de sincronización maneja reintentos

---

## Solución de Problemas

### El Service Worker no se registra

Verificar:
- HTTPS o localhost
- Ruta correcta del archivo sw.js
- No hay errores en consola

### Los datos no se sincronizan

Verificar:
- La API está accesible
- Las acciones están en la cola
- Hay conexión a internet

### El caché no se actualiza

Forzar actualización:
```js
// En consola
caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))
navigator.serviceWorker.ready.then(reg => reg.unregister())
location.reload()
```

---

## Próximos Pasos

Después de implementar PWA Offline:

1. **Fase 3**: Marketplace ultraligero
2. **Fase 4**: Geolocalización cubana con OpenStreetMap
3. **Fase 5**: Sistema WhatsApp-centric
4. **Fase 6**: Analíticas ligeras
5. **Fase 7**: Tu Merkadito Business
6. **Fase 8**: Tu Merkadito POS

---

## Recursos Adicionales

- [MDN: Progressive Web Apps](https://developer.mozilla.org/es/docs/Web/Progressive_web_apps)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [IndexedDB API](https://developer.mozilla.org/es/docs/Web/API/IndexedDB_API)
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/)
