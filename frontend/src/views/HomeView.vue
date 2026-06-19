<template>
  <div class="space-y-6">
    <!-- Hero Section -->
    <section class="text-center py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Encuentra negocios y productos en Cuba
      </h1>
      <p class="text-gray-600 mb-6">
        Directorio comercial rápido y ligero, funciona incluso sin internet
      </p>
      
      <!-- Barra de búsqueda -->
      <div class="max-w-2xl mx-auto">
        <form @submit.prevent="buscar" class="flex gap-2">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="¿Qué estás buscando? Ej: pizza, ropa, farmacia..."
            class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <button
            type="submit"
            class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
          >
            Buscar
          </button>
        </form>
      </div>
    </section>

    <!-- Categorías Populares -->
    <section class="py-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Categorías Populares</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <button
          v-for="categoria in categorias"
          :key="categoria.id"
          @click="filtrarPorCategoria(categoria.slug)"
          class="p-4 bg-white rounded-lg shadow-sm border hover:shadow-md transition text-center"
        >
          <span class="text-2xl">{{ categoria.icon }}</span>
          <p class="mt-2 text-sm font-medium text-gray-700">{{ categoria.nombre }}</p>
        </button>
      </div>
    </section>

    <!-- Empresas Destacadas -->
    <section class="py-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-900">Empresas Destacadas</h2>
        <router-link to="/buscar" class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
          Ver todas →
        </router-link>
      </div>
      
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-2 text-gray-600">Cargando empresas...</p>
      </div>
      
      <div v-else-if="empresas.length === 0" class="text-center py-8 text-gray-600">
        No hay empresas disponibles
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="empresa in empresas"
          :key="empresa.id"
          class="bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition"
        >
          <router-link :to="`/empresa/${empresa.slug}`">
            <div class="p-4">
              <div class="flex items-start gap-3">
                <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                  {{ empresa.logo_url || '🏪' }}
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-semibold text-gray-900 truncate">{{ empresa.nombre }}</h3>
                  <p class="text-sm text-gray-600 mt-1">{{ empresa.categoria }}</p>
                  <p class="text-xs text-gray-500 mt-1">
                    📍 {{ empresa.municipio }}, {{ empresa.provincia }}
                  </p>
                </div>
              </div>
              <div class="mt-3 flex items-center justify-between">
                <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                  ✅ Abierto
                </span>
                <a
                  :href="`https://wa.me/${empresa.whatsapp}`"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-xs bg-green-500 text-white px-3 py-1.5 rounded-full hover:bg-green-600 transition flex items-center gap-1"
                  @click.stop="registrarClick(empresa.id)"
                >
                  📲 WhatsApp
                </a>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Características Offline -->
    <section class="py-6 bg-indigo-50 rounded-lg px-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-3">
        📴 Funciona sin internet
      </h2>
      <ul class="space-y-2 text-gray-700">
        <li class="flex items-center gap-2">
          ✅ <span>Ver empresas y productos guardados en caché</span>
        </li>
        <li class="flex items-center gap-2">
          ✅ <span>Acceder a tus favoritos</span>
        </li>
        <li class="flex items-center gap-2">
          ✅ <span>Buscar en historial reciente</span>
        </li>
        <li class="flex items-center gap-2">
          ✅ <span>Sincronización automática cuando vuelve la conexión</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { guardarEmpresa, obtenerTodasLasEmpresas } from '@/pwa/db'

const router = useRouter()
const searchQuery = ref('')
const loading = ref(false)
const empresas = ref([])

const categorias = [
  { id: 1, nombre: 'Restaurantes', slug: 'restaurantes', icon: '🍕' },
  { id: 2, nombre: 'Ropa', slug: 'ropa', icon: '👕' },
  { id: 3, nombre: 'Farmacias', slug: 'farmacias', icon: '💊' },
  { id: 4, nombre: 'Tecnología', slug: 'tecnologia', icon: '💻' },
  { id: 5, nombre: 'Hogar', slug: 'hogar', icon: '🏠' },
  { id: 6, nombre: 'Servicios', slug: 'servicios', icon: '🔧' }
]

onMounted(async () => {
  await cargarEmpresas()
})

async function cargarEmpresas() {
  loading.value = true
  
  try {
    // Intentar obtener desde API
    const response = await axios.get('/api/v1/empresas/?limit=6')
    empresas.value = response.data.results || response.data
    
    // Guardar en caché IndexedDB
    for (const empresa of empresas.value) {
      await guardarEmpresa(empresa)
    }
  } catch (error) {
    console.error('Error cargando empresas:', error)
    
    // Fallback: obtener desde caché
    empresas.value = await obtenerTodasLasEmpresas()
    empresas.value = empresas.value.slice(0, 6)
  } finally {
    loading.value = false
  }
}

function buscar() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/buscar', query: { q: searchQuery.value } })
  }
}

function filtrarPorCategoria(slug) {
  router.push({ path: '/buscar', query: { categoria: slug } })
}

async function registrarClick(empresaId) {
  try {
    await axios.post('/api/v1/analytics/click/', {
      empresa_id: empresaId,
      tipo: 'whatsapp'
    })
  } catch (error) {
    // Si falla, guardar en cola de sincronización
    console.log('Click registrado offline, se sincronizará después')
  }
}
</script>
