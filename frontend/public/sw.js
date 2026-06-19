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
