<template>
  <div class="space-y-6">
    <!-- Título -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Buscar</h1>
      <span class="text-sm text-gray-600">{{ resultados.length }} resultado(s)</span>
    </div>

    <!-- Barra de búsqueda y filtros -->
    <SearchBar
      v-model="searchQuery"
      :initial-categoria="selectedCategoria"
      @search="aplicarFiltros"
      @filter="aplicarFiltroRapido"
    />

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Sidebar con filtros avanzados -->
      <aside class="lg:col-span-1">
        <Filters
          v-model="filtrosAvanzados"
          :es-desktop="true"
          @apply="aplicarFiltrosCompletos"
        />
      </aside>

      <!-- Resultados -->
      <main class="lg:col-span-3">
        <!-- Loading skeleton -->
        <div v-if="loading" class="space-y-4">
          <div v-for="i in 6" :key="i" class="bg-white rounded-lg shadow-sm border p-4 animate-pulse">
            <div class="flex gap-3">
              <div class="w-16 h-16 bg-gray-200 rounded-lg"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                <div class="h-3 bg-gray-200 rounded w-1/4"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sin resultados -->
        <div v-else-if="resultados.length === 0" class="text-center py-12 bg-white rounded-lg border">
          <div class="text-6xl mb-4">🔍</div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">
            No se encontraron resultados
          </h3>
          <p class="text-gray-600 mb-4">
            Intenta con otros términos o limpia los filtros
          </p>
          <button
            @click="limpiarBusqueda"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Ver todos
          </button>
        </div>

        <!-- Lista de empresas -->
        <div v-else class="space-y-4">
          <EmpresaCard
            v-for="empresa in resultados"
            :key="empresa.id"
            :empresa="empresa"
          />

          <!-- Infinite scroll loader -->
          <div v-if="cargandoMas" class="text-center py-4">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600 mx-auto"></div>
            <p class="text-sm text-gray-600 mt-2">Cargando más...</p>
          </div>

          <!-- Fin de resultados -->
          <div v-if="!tieneMas && resultados.length > 0" class="text-center py-4 text-gray-600">
            <p>No hay más resultados</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'
import Filters from '@/components/Filters.vue'
import EmpresaCard from '@/components/EmpresaCard.vue'
import { guardarEmpresa, obtenerTodasLasEmpresas, guardarBusqueda } from '@/pwa/db'
import { useFavoritesStore } from '@/stores/favorites'

const route = useRoute()
const favoritesStore = useFavoritesStore()

const searchQuery = ref('')
const selectedCategoria = ref(route.query.categoria || '')
const filtrosAvanzados = ref({
  provincia: '',
  municipio: '',
  activo: false,
  orden: '-creado_en'
})

const loading = ref(false)
const cargandoMas = ref(false)
const resultados = ref([])
const pagina = ref(1)
const tieneMas = ref(true)

onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q
  }
  aplicarFiltros()
})

async function aplicarFiltros(params = {}) {
  loading.value = true
  pagina.value = 1
  
  try {
    const queryParams = new URLSearchParams()
    
    if (searchQuery.value) {
      queryParams.set('search', searchQuery.value)
    }
    if (selectedCategoria.value) {
      queryParams.set('categoria__slug', selectedCategoria.value)
    }
    if (filtrosAvanzados.value.provincia) {
      queryParams.set('provincia', filtrosAvanzados.value.provincia)
    }
    if (filtrosAvanzados.value.municipio) {
      queryParams.set('municipio', filtrosAvanzados.value.municipio)
    }
    if (filtrosAvanzados.value.activo) {
      queryParams.set('activo', 'true')
    }
    if (filtrosAvanzados.value.orden) {
      queryParams.set('ordering', filtrosAvanzados.value.orden)
    }
    queryParams.set('page', pagina.value)
    queryParams.set('limit', 20)

    const response = await axios.get(`/api/v1/empresas/?${queryParams.toString()}`)
    
    resultados.value = response.data.results || response.data
    tieneMas.value = !!response.data.next
    
    // Guardar en caché offline
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

async function cargarMas() {
  if (cargandoMas.value || !tieneMas.value) return
  
  cargandoMas.value = true
  pagina.value++
  
  try {
    const queryParams = new URLSearchParams()
    if (searchQuery.value) queryParams.set('search', searchQuery.value)
    if (selectedCategoria.value) queryParams.set('categoria__slug', selectedCategoria.value)
    queryParams.set('page', pagina.value)
    queryParams.set('limit', 20)
    
    const response = await axios.get(`/api/v1/empresas/?${queryParams.toString()}`)
    const nuevos = response.data.results || response.data
    
    resultados.value = [...resultados.value, ...nuevos]
    tieneMas.value = !!response.data.next
    
    for (const empresa of nuevos) {
      await guardarEmpresa(empresa)
    }
  } catch (error) {
    console.error('Error cargando más:', error)
  } finally {
    cargandoMas.value = false
  }
}

function aplicarFiltroRapido({ query, categoria }) {
  searchQuery.value = query || ''
  selectedCategoria.value = categoria || ''
  aplicarFiltros()
}

function aplicarFiltrosCompletos(nuevosFiltros) {
  filtrosAvanzados.value = { ...filtrosAvanzados.value, ...nuevosFiltros }
  aplicarFiltros()
}

function filtrarLocalmente(empresas) {
  return empresas.filter(empresa => {
    const matchSearch = !searchQuery.value || 
      empresa.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCategoria = !selectedCategoria.value || empresa.categoria === selectedCategoria.value
    return matchSearch && matchCategoria
  })
}

function limpiarBusqueda() {
  searchQuery.value = ''
  selectedCategoria.value = ''
  filtrosAvanzados.value = {
    provincia: '',
    municipio: '',
    activo: false,
    orden: '-creado_en'
  }
  aplicarFiltros()
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
</script>
