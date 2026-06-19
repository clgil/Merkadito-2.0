import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { initDB } from './pwa/db'
import { useOfflineStore } from './stores/offline'
import './assets/main.css'

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
  })
}

// Inicializar store offline
const offlineStore = useOfflineStore(pinia)
offlineStore.setOnline(navigator.onLine)

app.mount('#app')
