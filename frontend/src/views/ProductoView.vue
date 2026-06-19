<template>
  <div class="space-y-6">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Cargando producto...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-600">{{ error }}</p>
      <router-link to="/" class="mt-4 inline-block text-indigo-600 hover:text-indigo-700">
        ← Volver al inicio
      </router-link>
    </div>

    <!-- Producto -->
    <div v-else-if="producto" class="max-w-4xl mx-auto">
      <!-- Card principal -->
      <div class="bg-white rounded-lg shadow-sm border overflow-hidden">
        <!-- Imagen -->
        <div class="aspect-video bg-gray-100 relative">
          <img
            v-if="producto.imagen"
            :src="producto.imagen"
            :alt="producto.nombre"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-6xl text-gray-400">
            📦
          </div>
          
          <!-- Badge disponibilidad -->
          <span
            :class="[
              'absolute top-4 right-4 px-3 py-1.5 rounded-full text-sm font-medium',
              producto.disponible
                ? 'bg-green-500 text-white'
                : 'bg-gray-500 text-white'
            ]"
          >
            {{ producto.disponible ? '✅ Disponible' : '⏸ No disponible' }}
          </span>
        </div>

        <!-- Contenido -->
        <div class="p-6">
          <!-- Título y precio -->
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">
                {{ producto.nombre }}
              </h1>
              <p v-if="producto.categoria" class="text-sm text-gray-600 mt-1">
                🏷️ {{ producto.categoria }}
              </p>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-indigo-600">
                ${{ producto.precio }}
              </div>
              <div class="text-sm text-gray-500">
                {{ producto.moneda }}
              </div>
            </div>
          </div>

          <!-- Descripción -->
          <div v-if="producto.descripcion_corta" class="mb-6">
            <h2 class="font-semibold text-gray-900 mb-2">Descripción</h2>
            <p class="text-gray-700 leading-relaxed">
              {{ producto.descripcion_corta }}
            </p>
          </div>

          <!-- Empresa -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-lg flex items-center justify-center text-xl">
                  🏪
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">
                    {{ producto.empresa?.nombre }}
                  </h3>
                  <p class="text-sm text-gray-600">
                    📍 {{ producto.empresa?.municipio }}, {{ producto.empresa?.provincia }}
                  </p>
                </div>
              </div>
              <router-link
                :to="`/empresa/${producto.empresa?.slug}`"
                class="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
              >
                Ver negocio →
              </router-link>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="flex flex-col sm:flex-row gap-3">
            <a
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="flex-1 bg-green-500 text-white py-3 px-6 rounded-lg hover:bg-green-600 transition font-medium flex items-center justify-center gap-2"
              @click="registrarClick"
            >
              📲 Consultar por WhatsApp
            </a>
            <button
              @click="toggleFavorite"
              :class="[
                'px-6 py-3 rounded-lg font-medium transition flex items-center justify-center gap-2',
                esFavorito
                  ? 'bg-red-50 text-red-600 border border-red-200'
                  : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
              ]"
            >
              {{ esFavorito ? '❤️' : '🤍' }} Favorito
            </button>
          </div>
        </div>
      </div>

      <!-- Productos relacionados -->
      <div v-if="productosRelacionados.length > 0" class="mt-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">
          Productos similares
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <ProductoCard
            v-for="prod in productosRelacionados"
            :key="prod.id"
            :producto="prod"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ProductoCard from '@/components/ProductoCard.vue'
import { guardarProducto, obtenerProducto, obtenerProductosPorCategoria } from '@/pwa/db'
import { useFavoritesStore } from '@/stores/favorites'

const route = useRoute()
const favoritesStore = useFavoritesStore()

const producto = ref(null)
const loading = ref(true)
const error = ref(null)
const productosRelacionados = ref([])

const whatsappLink = computed(() => {
  if (!producto.value?.empresa?.whatsapp) return '#'
  
  const numero = producto.value.empresa.whatsapp
  const mensaje = `Hola, me interesa el producto: ${producto.value.nombre} (Precio: $${producto.value.precio} ${producto.value.moneda})`
  const numeroLimpio = numero.replace('+', '').replace(' ', '').replace('-', '')
  return `https://wa.me/${numeroLimpio}?text=${encodeURIComponent(mensaje)}`
})

const esFavorito = computed(() => {
  if (!producto.value) return false
  return favoritesStore.isFavorite(producto.value.empresa?.id)
})

onMounted(async () => {
  await cargarProducto()
})

async function cargarProducto() {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`/api/v1/productos/${route.params.id}/`)
    producto.value = response.data
    
    // Guardar en caché
    await guardarProducto(producto.value)
    
    // Cargar productos relacionados
    await cargarRelacionados()
  } catch (err) {
    console.error('Error cargando producto:', err)
    
    // Fallback offline
    const cached = await obtenerProducto(route.params.id)
    if (cached) {
      producto.value = cached
    } else {
      error.value = 'No se pudo cargar el producto. Verifica tu conexión.'
    }
  } finally {
    loading.value = false
  }
}

async function cargarRelacionados() {
  if (!producto.value?.categoria) return
  
  try {
    const response = await axios.get(
      `/api/v1/productos/?categoria=${producto.value.categoria}&limit=6`
    )
    const todos = response.data.results || response.data
    
    // Excluir el producto actual
    productosRelacionados.value = todos.filter(p => p.id !== producto.value.id).slice(0, 3)
    
    for (const prod of productosRelacionados.value) {
      await guardarProducto(prod)
    }
  } catch (err) {
    console.error('Error cargando relacionados:', err)
  }
}

function toggleFavorite() {
  if (!producto.value?.empresa) return
  
  favoritesStore.toggleFavorite({
    id: producto.value.empresa.id,
    nombre: producto.value.empresa.nombre,
    slug: producto.value.empresa.slug,
    categoria: producto.value.empresa.categoria,
    whatsapp: producto.value.empresa.whatsapp
  })
}

async function registrarClick() {
  try {
    await axios.post('/api/v1/analytics/click/', {
      producto_id: producto.value.id,
      empresa_id: producto.value.empresa?.id,
      tipo: 'whatsapp_producto'
    })
  } catch (err) {
    console.log('Click registrado offline')
  }
}
</script>
