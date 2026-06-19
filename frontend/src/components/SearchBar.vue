<template>
  <div class="bg-white rounded-lg shadow-sm border p-4">
    <div class="flex items-center gap-3 mb-4">
      <input
        v-model="query"
        @input="handleInput"
        type="text"
        placeholder="¿Qué estás buscando? Ej: pizza, ropa, farmacia..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
      />
      <button
        @click="buscar"
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
      >
        🔍
      </button>
    </div>

    <!-- Filtros rápidos -->
    <div class="flex flex-wrap gap-2">
      <button
        v-for="cat in categorias"
        :key="cat.slug"
        @click="seleccionarCategoria(cat.slug)"
        :class="[
          'px-3 py-1.5 rounded-full text-sm transition',
          categoriaActiva === cat.slug
            ? 'bg-indigo-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        {{ cat.icon }} {{ cat.nombre }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  initialCategoria: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'filter'])

const query = ref(props.modelValue)
const categoriaActiva = ref(props.initialCategoria)
let debounceTimer = null

const categorias = [
  { nombre: 'Todas', slug: '', icon: '🔍' },
  { nombre: 'Restaurantes', slug: 'restaurantes', icon: '🍕' },
  { nombre: 'Ropa', slug: 'ropa', icon: '👕' },
  { nombre: 'Farmacias', slug: 'farmacias', icon: '💊' },
  { nombre: 'Tecnología', slug: 'tecnologia', icon: '💻' },
  { nombre: 'Hogar', slug: 'hogar', icon: '🏠' },
  { nombre: 'Servicios', slug: 'servicios', icon: '🔧' }
]

watch(() => props.modelValue, (newVal) => {
  query.value = newVal
})

function handleInput() {
  emit('update:modelValue', query.value)
  
  // Debounce para búsqueda automática
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    if (query.value.trim().length >= 2) {
      buscar()
    }
  }, 300)
}

function buscar() {
  emit('search', { query: query.value, categoria: categoriaActiva.value })
}

function seleccionarCategoria(slug) {
  categoriaActiva.value = slug
  emit('filter', { categoria: slug, query: query.value })
}
</script>
