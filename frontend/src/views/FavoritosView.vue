<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900">❤️ Favoritos</h1>

    <div v-if="favoritesStore.loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Cargando favoritos...</p>
    </div>

    <div v-else-if="favoritesStore.favorites.length === 0" class="text-center py-12 bg-white rounded-lg border">
      <p class="text-6xl mb-4">🤍</p>
      <p class="text-gray-600 text-lg">No tienes favoritos guardados</p>
      <p class="text-sm text-gray-500 mt-2">Explora empresas y productos para agregarlos a tus favoritos</p>
      <router-link to="/buscar" class="inline-block mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
        Explorar directorio
      </router-link>
    </div>

    <div v-else class="space-y-4">
      <p class="text-sm text-gray-600">{{ favoritesStore.count }} favorito(s)</p>

      <div
        v-for="fav in favoritesStore.favorites"
        :key="fav.id"
        class="bg-white rounded-lg shadow-sm border p-4 hover:shadow-md transition"
      >
        <router-link :to="`/empresa/${fav.slug}`" class="block">
          <div class="flex items-start justify-between">
            <div class="flex items-start gap-4 flex-1">
              <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                {{ fav.logo_url || '🏪' }}
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-900">{{ fav.nombre }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ fav.categoria }}</p>
                <p v-if="fav.whatsapp" class="text-xs text-gray-500 mt-1">
                  📱 {{ fav.whatsapp }}
                </p>
              </div>
            </div>
            
            <button
              @click.prevent="eliminarFavorito(fav.id)"
              class="text-red-500 hover:text-red-700 transition p-2"
              title="Eliminar de favoritos"
            >
              ❌
            </button>
          </div>
        </router-link>
        
        <div class="mt-4">
          <a
            v-if="fav.whatsapp"
            :href="`https://wa.me/${fav.whatsapp}`"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition text-sm"
          >
            📲 Contactar por WhatsApp
          </a>
        </div>
      </div>
    </div>

    <!-- Información Offline -->
    <div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
      <h3 class="font-medium text-blue-900 mb-2">💾 Tus favoritos se guardan offline</h3>
      <p class="text-sm text-blue-700">
        Esta información se almacena en tu dispositivo y está disponible incluso sin conexión a internet.
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFavoritesStore } from '@/stores/favorites'

const favoritesStore = useFavoritesStore()

onMounted(() => {
  favoritesStore.loadFavorites()
})

function eliminarFavorito(id) {
  favoritesStore.removeFavorite(id)
}
</script>
