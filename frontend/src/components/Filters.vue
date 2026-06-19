<template>
  <div class="bg-white rounded-lg shadow-sm border p-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-semibold text-gray-900">Filtros</h3>
      <button
        @click="colapsar = !colapsar"
        class="text-gray-500 hover:text-gray-700 lg:hidden"
      >
        {{ colapsar ? '▶' : '▼' }}
      </button>
    </div>

    <div v-show="!colapsar || esDesktop" class="space-y-4">
      <!-- Categoría -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Categoría
        </label>
        <select
          v-model="filtroLocal.categoria"
          @change="aplicarFiltros"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todas las categorías</option>
          <option v-for="cat in categorias" :key="cat.slug" :value="cat.slug">
            {{ cat.nombre }}
          </option>
        </select>
      </div>

      <!-- Provincia -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Provincia
        </label>
        <select
          v-model="filtroLocal.provincia"
          @change="aplicarFiltros"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todas las provincias</option>
          <option v-for="prov in provincias" :key="prov.id" :value="prov.id">
            {{ prov.nombre }}
          </option>
        </select>
      </div>

      <!-- Municipio (depende de provincia) -->
      <div v-if="filtroLocal.provincia">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Municipio
        </label>
        <select
          v-model="filtroLocal.municipio"
          @change="aplicarFiltros"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todos los municipios</option>
          <option v-for="mun in municipiosFiltrados" :key="mun.id" :value="mun.id">
            {{ mun.nombre }}
          </option>
        </select>
      </div>

      <!-- Disponibilidad -->
      <div>
        <label class="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            v-model="filtroLocal.activo"
            @change="aplicarFiltros"
            class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
          />
          <span class="text-sm text-gray-700">Solo activos/abiertos</span>
        </label>
      </div>

      <!-- Ordenamiento -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Ordenar por
        </label>
        <select
          v-model="filtroLocal.orden"
          @change="aplicarFiltros"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="-creado_en">Más recientes</option>
          <option value="nombre">Nombre (A-Z)</option>
          <option value="-nombre">Nombre (Z-A)</option>
        </select>
      </div>

      <!-- Botón limpiar -->
      <button
        @click="limpiarFiltros"
        class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm font-medium"
      >
        🗑️ Limpiar filtros
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  esDesktop: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'apply'])

const colapsar = ref(false)
const categorias = ref([])
const provincias = ref([])
const municipios = ref([])

const filtroLocal = ref({
  categoria: '',
  provincia: '',
  municipio: '',
  activo: false,
  orden: '-creado_en'
})

const municipiosFiltrados = computed(() => {
  if (!filtroLocal.value.provincia) return []
  return municipios.value.filter(
    m => m.provincia_id === parseInt(filtroLocal.value.provincia)
  )
})

// Cargar datos iniciales
async function cargarDatos() {
  try {
    const [catsResponse, provsResponse] = await Promise.all([
      axios.get('/api/v1/categorias/'),
      axios.get('/api/v1/provincias/')
    ])
    categorias.value = catsResponse.data
    provincias.value = provsResponse.data
  } catch (error) {
    console.error('Error cargando filtros:', error)
  }
}

watch(() => filtroLocal.value.provincia, async () => {
  filtroLocal.value.municipio = ''
  if (filtroLocal.value.provincia) {
    try {
      const response = await axios.get(
        `/api/v1/municipios/?provincia=${filtroLocal.value.provincia}`
      )
      municipios.value = response.data
    } catch (error) {
      console.error('Error cargando municipios:', error)
    }
  } else {
    municipios.value = []
  }
})

function aplicarFiltros() {
  emit('update:modelValue', filtroLocal.value)
  emit('apply', filtroLocal.value)
}

function limpiarFiltros() {
  filtroLocal.value = {
    categoria: '',
    provincia: '',
    municipio: '',
    activo: false,
    orden: '-creado_en'
  }
  aplicarFiltros()
}

// Inicializar
cargarDatos()
</script>
