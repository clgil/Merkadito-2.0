<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900">📴 Sin conexión</h1>

    <div class="bg-white rounded-lg shadow-sm border p-8 text-center">
      <p class="text-6xl mb-4">📴</p>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        No tienes conexión a internet
      </h2>
      <p class="text-gray-600 mb-6">
        Puedes seguir navegando por el contenido guardado en caché
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 class="font-medium text-green-900 mb-2">✅ Disponible offline</h3>
          <ul class="space-y-1 text-sm text-green-700">
            <li>• Empresas visitadas recientemente</li>
            <li>• Tus favoritos guardados</li>
            <li>• Historial de búsquedas</li>
            <li>• Productos en caché</li>
          </ul>
        </div>

        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 class="font-medium text-yellow-900 mb-2">⚠️ Requiere conexión</h3>
          <ul class="space-y-1 text-sm text-yellow-700">
            <li>• Nuevas búsquedas</li>
            <li>• Datos actualizados</li>
            <li>• Contactar por WhatsApp</li>
            <li>• Sincronizar cambios</li>
          </ul>
        </div>
      </div>

      <button
        @click="verificarConexion"
        class="mt-8 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
      >
        🔄 Verificar conexión
      </button>

      <p v-if="lastSync" class="mt-4 text-sm text-gray-500">
        Última sincronización: {{ formatLastSync(lastSync) }}
      </p>
    </div>

    <!-- Contenido offline disponible -->
    <div v-if="empresasCache.length > 0" class="mt-8">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">
        Empresas en caché ({{ empresasCache.length }})
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <router-link
          v-for="empresa in empresasCache"
          :key="empresa.id"
          :to="`/empresa/${empresa.slug}`"
          class="bg-white rounded-lg shadow-sm border p-4 hover:shadow-md transition"
        >
          <div class="flex items-start gap-3">
            <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center text-xl flex-shrink-0">
              {{ empresa.logo_url || '🏪' }}
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-gray-900 truncate">{{ empresa.nombre }}</h3>
              <p class="text-xs text-gray-500 mt-1">{{ empresa.categoria }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOfflineStore } from '@/stores/offline'
import { obtenerTodasLasEmpresas } from '@/pwa/db'

const offlineStore = useOfflineStore()
const empresasCache = ref([])
const lastSync = ref(null)

onMounted(async () => {
  empresasCache.value = await obtenerTodasLasEmpresas()
  lastSync.value = offlineStore.lastSyncTime
})

function verificarConexion() {
  if (navigator.onLine) {
    window.location.reload()
  } else {
    alert('Sigue sin conexión. Verifica tu conexión a internet.')
  }
}

function formatLastSync(timestamp) {
  if (!timestamp) return 'Nunca'
  const date = new Date(timestamp)
  return date.toLocaleString('es-CU')
}
</script>
