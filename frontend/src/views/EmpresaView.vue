<template>
  <div class="space-y-6">
    <!-- Header de la empresa -->
    <div v-if="empresa" class="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div class="bg-gradient-to-r from-indigo-500 to-purple-600 h-32"></div>
      <div class="px-6 pb-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-end -mt-12 gap-4">
          <div class="w-24 h-24 bg-white rounded-xl shadow-md flex items-center justify-center text-4xl flex-shrink-0">
            {{ empresa.logo_url || '🏪' }}
          </div>
          <div class="flex-1 pt-2">
            <h1 class="text-2xl font-bold text-gray-900">{{ empresa.nombre }}</h1>
            <p class="text-gray-600 mt-1">{{ empresa.categoria }}</p>
            <p class="text-sm text-gray-500 mt-1">
              📍 {{ empresa.direccion }}, {{ empresa.municipio }}, {{ empresa.provincia }}
            </p>
          </div>
          <div class="flex gap-2">
            <button
              @click="toggleFavorite(empresa)"
              class="p-3 rounded-full border hover:bg-gray-50 transition"
              :class="{ 'bg-red-50 border-red-200': esFavorito(empresa.id) }"
            >
              {{ esFavorito(empresa.id) ? '❤️' : '🤍' }}
            </button>
            <a
              v-if="empresa.whatsapp"
              :href="`https://wa.me/${empresa.whatsapp}`"
              target="_blank"
              rel="noopener noreferrer"
              class="px-4 py-3 bg-green-500 text-white rounded-full hover:bg-green-600 transition font-medium flex items-center gap-2"
              @click="registrarClick(empresa.id)"
            >
              📲 WhatsApp
            </a>
          </div>
        </div>

        <div v-if="empresa.descripcion" class="mt-6 pt-6 border-t">
          <h2 class="font-semibold text-gray-900 mb-2">Descripción</h2>
          <p class="text-gray-700">{{ empresa.descripcion }}</p>
        </div>

        <div class="mt-6 flex flex-wrap gap-4 text-sm text-gray-600">
          <div v-if="empresa.telefono" class="flex items-center gap-2">
            <span>📞</span>
            <a :href="`tel:${empresa.telefono}`" class="hover:text-indigo-600">
              {{ empresa.telefono }}
            </a>
          </div>
          <div class="flex items-center gap-2">
            <span>✅</span>
            <span>Abierto ahora</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Productos -->
    <div v-if="empresa" class="mt-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Productos</h2>

      <div v-if="loadingProductos" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-2 text-gray-600">Cargando productos...</p>
      </div>

      <div v-else-if="productos.length === 0" class="text-center py-8 bg-white rounded-lg border">
        <p class="text-gray-600">Esta empresa no tiene productos publicados</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="producto in productos"
          :key="producto.id"
          class="bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition"
        >
          <div class="h-40 bg-gray-200 flex items-center justify-center text-4xl">
            {{ producto.imagen_url || '📦' }}
          </div>
          <div class="p-4">
            <h3 class="font-medium text-gray-900">{{ producto.nombre }}</h3>
            <p v-if="producto.descripcion_corta" class="text-sm text-gray-600 mt-1 line-clamp-2">
              {{ producto.descripcion_corta }}
            </p>
            <div class="mt-3 flex items-center justify-between">
              <span class="text-lg font-bold text-indigo-600">
                {{ formatoMoneda(producto.precio, producto.moneda) }}
              </span>
              <span
                v-if="producto.disponible"
                class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full"
              >
                Disponible
              </span>
              <span
                v-else
                class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded-full"
              >
                No disponible
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error / Cargando -->
    <div v-if="error" class="text-center py-12">
      <p class="text-red-600">{{ error }}</p>
      <router-link to="/" class="mt-4 inline-block text-indigo-600 hover:text-indigo-700">
        ← Volver al inicio
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Cargando empresa...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { guardarEmpresa, obtenerEmpresa, obtenerProductosPorEmpresa, guardarProducto } from '@/pwa/db'
import { useFavoritesStore } from '@/stores/favorites'

const route = useRoute()
const favoritesStore = useFavoritesStore()

const empresa = ref(null)
const productos = ref([])
const loading = ref(true)
const loadingProductos = ref(false)
const error = ref(null)

onMounted(async () => {
  await cargarEmpresa()
})

async function cargarEmpresa() {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`/api/v1/empresas/${route.params.slug}/`)
    empresa.value = response.data
    
    // Guardar en caché
    await guardarEmpresa(empresa.value)
    
    // Cargar productos
    await cargarProductos()
  } catch (err) {
    console.error('Error cargando empresa:', err)
    
    // Fallback offline
    const cached = await obtenerEmpresa(route.params.slug)
    if (cached) {
      empresa.value = cached
      await cargarProductosOffline()
    } else {
      error.value = 'No se pudo cargar la empresa. Verifica tu conexión.'
    }
  } finally {
    loading.value = false
  }
}

async function cargarProductos() {
  if (!empresa.value) return
  
  loadingProductos.value = true
  
  try {
    const response = await axios.get(`/api/v1/productos/?empresa=${empresa.value.id}`)
    productos.value = response.data.results || response.data
    
    // Guardar en caché
    for (const producto of productos.value) {
      await guardarProducto(producto)
    }
  } catch (err) {
    console.error('Error cargando productos:', err)
    await cargarProductosOffline()
  } finally {
    loadingProductos.value = false
  }
}

async function cargarProductosOffline() {
  if (!empresa.value) return
  productos.value = await obtenerProductosPorEmpresa(empresa.value.id)
}

function formatoMoneda(precio, moneda) {
  const simbolos = {
    CUP: '$',
    USD: 'US$',
    MLC: 'MLC'
  }
  return `${simbolos[moneda] || '$'}${precio}`
}

function esFavorito(id) {
  return favoritesStore.isFavorite(id)
}

function toggleFavorite(emp) {
  favoritesStore.toggleFavorite({
    id: emp.id,
    nombre: emp.nombre,
    slug: emp.slug,
    categoria: emp.categoria,
    whatsapp: emp.whatsapp,
    logo_url: emp.logo_url
  })
}

async function registrarClick(empresaId) {
  try {
    await axios.post('/api/v1/analytics/click/', {
      empresa_id: empresaId,
      tipo: 'whatsapp'
    })
  } catch (err) {
    console.log('Click registrado offline')
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
