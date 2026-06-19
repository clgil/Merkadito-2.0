<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Banner Offline -->
    <OfflineBanner @retry="syncData" />

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          <router-link to="/" class="text-xl font-bold text-indigo-600">
            🛒 Tu Merkadito
          </router-link>
          
          <nav class="flex items-center gap-4">
            <router-link 
              to="/buscar" 
              class="text-gray-600 hover:text-indigo-600 transition"
            >
              🔍 Buscar
            </router-link>
            <router-link 
              to="/favoritos" 
              class="text-gray-600 hover:text-indigo-600 transition"
            >
              ❤️ Favoritos
              <span v-if="favoritesCount > 0" class="ml-1 text-sm">({{ favoritesCount }})</span>
            </router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="max-w-7xl mx-auto px-4 py-6">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t mt-12">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <div class="text-center text-gray-600 text-sm">
          <p>© {{ currentYear }} Tu Merkadito - Directorio Comercial de Cuba</p>
          <p class="mt-2">
            Funciona offline 📴 | Optimizado para datos móviles 📱
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useFavoritesStore } from './stores/favorites'
import { useOfflineStore } from './stores/offline'
import OfflineBanner from './components/OfflineBanner.vue'
import { syncFreshData } from './pwa/sync'

const favoritesStore = useFavoritesStore()
const offlineStore = useOfflineStore()

const favoritesCount = computed(() => favoritesStore.count)
const currentYear = new Date().getFullYear()

onMounted(async () => {
  // Cargar favoritos desde IndexedDB
  await favoritesStore.loadFavorites()
  
  // Si hay conexión, sincronizar datos frescos
  if (offlineStore.isOnline) {
    await syncFreshData()
  }
})

async function syncData() {
  if (offlineStore.isOnline) {
    await syncFreshData()
    offlineStore.setLastSyncTime(new Date().toISOString())
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
