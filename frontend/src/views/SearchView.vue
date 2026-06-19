<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900">Buscar</h1>
    
    <!-- Filtros -->
    <div class="bg-white p-4 rounded-lg shadow-sm border space-y-4">
      <div>
        <input
          v-model="searchQuery"
          @input="debouncedSearch"
          type="text"
          placeholder="Buscar por nombre o descripción..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <select
          v-model="selectedCategoria"
          @change="aplicarFiltros"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todas las categorías</option>
          <option v-for="cat in categorias" :key="cat.slug" :value="cat.slug">
            {{ cat.nombre }}
          </option>
        </select>
        
        <select
          v-model="selectedProvincia"
          @change="aplicarFiltros"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todas las provincias</option>
          <option v-for="prov in provincias" :key="prov" :value="prov">
            {{ prov }}
          </option>
        </select>
      </div>
    </div>

    <!-- Resultados -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Buscando...</p>
    </div>

    <div v-else-if="resultados.length === 0" class="text-center py-12 bg-white rounded-lg border">
      <p class="text-gray-600">No se encontraron resultados</p>
      <p class="text-sm text-gray-500 mt-2">Intenta con otros términos de búsqueda</p>
    </div>

    <div v-else class="space-y-4">
      <p class="text-sm text-gray-600">{{ resultados.length }} resultado(s)</p>
      
      <div
        v-for="empresa in resultados"
        :key="empresa.id"
        class="bg-white rounded-lg shadow-sm border p-4 hover:shadow-md transition"
      >
        <router-link :to="`/empresa/${empresa.slug}`" class="block">
          <div class="flex items-start gap-4">
            <div class="w-20 h-20 bg-gray-200 rounded-lg flex items-center justify-center text-3xl flex-shrink-0">
              {{ empresa.logo_url || '🏪' }}
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-900 text-lg">{{ empresa.nombre }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ empresa.descripcion_corta }}</p>
              <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span>📍 {{ empresa.municipio }}, {{ empresa.provincia }}</span>
                <span class="bg-green-100 text-green-800 px-2 py-0.5 rounded-full text-xs">
                  {{ empresa.categoria }}
                </span>
              </div>
            </div>
          </div>
        </router-link>
        
        <div class="mt-4 flex items-center justify-between">
          <button
            @click="toggleFavorite(empresa)"
            class="text-gray-600 hover:text-red-500 transition"
            :class="{ 'text-red-500': esFavorito(empresa.id) }"
          >
            {{ esFavorito(empresa.id) ? '❤️' : '🤍' }} Favorito
          </button>
          
          <a
            :href="`https://wa.me/${empresa.whatsapp}`"
            target="_blank"
            rel="noopener noreferrer"
            class="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition flex items-center gap-2 text-sm"
            @click="registrarClick(empresa.id)"
          >
            📲 Contactar por WhatsApp
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { guardarEmpresa, obtenerTodasLasEmpresas, guardarBusqueda } from '@/pwa/db'
import { useFavoritesStore } from '@/stores/favorites'

const route = useRoute()
const favoritesStore = useFavoritesStore()

const searchQuery = ref('')
const selectedCategoria = ref('')
const selectedProvincia = ref('')
const loading = ref(false)
const resultados = ref([])

const categorias = [
  { nombre: 'Restaurantes', slug: 'restaurantes' },
  { nombre: 'Ropa', slug: 'ropa' },
  { nombre: 'Farmacias', slug: 'farmacias' },
  { nombre: 'Tecnología', slug: 'tecnologia' },
  { nombre: 'Hogar', slug: 'hogar' },
  { nombre: 'Servicios', slug: 'servicios' }
]

const provincias = [
  'Pinar del Río',
  'Artemisa',
  'La Habana',
  'Mayabeque',
  'Matanzas',
  'Cienfuegos',
  'Villa Clara',
  'Sancti Spíritus',
  'Ciego de Ávila',
  'Camagüey',
  'Las Tunas',
  'Holguín',
  'Granma',
  'Santiago de Cuba',
  'Guantánamo'
]

let searchTimeout = null

onMounted(() => {
  // Leer parámetros de URL
  if (route.query.q) {
    searchQuery.value = route.query.q
  }
  if (route.query.categoria) {
    selectedCategoria.value = route.query.categoria
  }
  
  aplicarFiltros()
})

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    aplicarFiltros()
  }, 500)
}

async function aplicarFiltros() {
  loading.value = true
  
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedCategoria.value) params.append('categoria', selectedCategoria.value)
    if (selectedProvincia.value) params.append('provincia', selectedProvincia.value)
    
    const response = await axios.get(`/api/v1/empresas/?${params.toString()}`)
    resultados.value = response.data.results || response.data
    
    // Guardar en caché
    for (const empresa of resultados.value) {
      await guardarEmpresa(empresa)
    }
    
    // Guardar búsqueda en historial
    if (searchQuery.value) {
      await guardarBusqueda(searchQuery.value, resultados.value)
    }
  } catch (error) {
    console.error('Error buscando:', error)
    
    // Fallback offline
    const todas = await obtenerTodasLasEmpresas()
    resultados.value = filtrarLocalmente(todas)
  } finally {
    loading.value = false
  }
}

function filtrarLocalmente(empresas) {
  return empresas.filter(empresa => {
    const matchSearch = !searchQuery.value || 
      empresa.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (empresa.descripcion && empresa.descripcion.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    const matchCategoria = !selectedCategoria.value || empresa.categoria === selectedCategoria.value
    const matchProvincia = !selectedProvincia.value || empresa.provincia === selectedProvincia.value
    
    return matchSearch && matchCategoria && matchProvincia
  })
}

function esFavorito(id) {
  return favoritesStore.isFavorite(id)
}

function toggleFavorite(empresa) {
  favoritesStore.toggleFavorite({
    id: empresa.id,
    nombre: empresa.nombre,
    slug: empresa.slug,
    categoria: empresa.categoria,
    whatsapp: empresa.whatsapp
  })
}

async function registrarClick(empresaId) {
  try {
    await axios.post('/api/v1/analytics/click/', {
      empresa_id: empresaId,
      tipo: 'whatsapp'
    })
  } catch (error) {
    console.log('Click registrado offline')
  }
}
</script>
