<template>
  <div class="bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition">
    <router-link :to="`/producto/${producto.id}`" class="block">
      <!-- Imagen -->
      <div class="relative aspect-square bg-gray-100 overflow-hidden">
        <img
          v-if="producto.imagen"
          :src="producto.imagen"
          :alt="producto.nombre"
          loading="lazy"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-400">
          📦
        </div>
        
        <!-- Badge disponible -->
        <span
          v-if="producto.disponible"
          class="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full"
        >
          Disponible
        </span>
        <span
          v-else
          class="absolute top-2 right-2 bg-gray-500 text-white text-xs px-2 py-1 rounded-full"
        >
          No disponible
        </span>
      </div>

      <!-- Contenido -->
      <div class="p-4">
        <h3 class="font-semibold text-gray-900 truncate mb-1">
          {{ producto.nombre }}
        </h3>
        
        <p v-if="producto.descripcion_corta" class="text-sm text-gray-600 line-clamp-2 mb-2">
          {{ producto.descripcion_corta }}
        </p>

        <!-- Precio -->
        <div class="flex items-baseline gap-1 mb-2">
          <span class="text-lg font-bold text-indigo-600">
            ${{ producto.precio }}
          </span>
          <span class="text-xs text-gray-500">
            {{ producto.moneda }}
          </span>
        </div>

        <!-- Empresa -->
        <div class="flex items-center gap-2 text-xs text-gray-500 mb-3">
          <span>🏪</span>
          <span class="truncate">{{ producto.empresa_nombre }}</span>
        </div>

        <!-- Botón WhatsApp -->
        <a
          :href="whatsappLink"
          target="_blank"
          rel="noopener noreferrer"
          class="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition flex items-center justify-center gap-2 text-sm font-medium"
          @click.stop="registrarClick"
        >
          📲 Consultar por WhatsApp
        </a>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  producto: {
    type: Object,
    required: true
  }
})

const whatsappLink = computed(() => {
  const numero = props.producto.empresa?.whatsapp || ''
  const mensaje = `Hola, me interesa el producto: ${props.producto.nombre}`
  const numeroLimpio = numero.replace('+', '').replace(' ', '').replace('-', '')
  return `https://wa.me/${numeroLimpio}?text=${encodeURIComponent(mensaje)}`
})

async function registrarClick() {
  try {
    await axios.post('/api/v1/analytics/click/', {
      producto_id: props.producto.id,
      empresa_id: props.producto.empresa?.id,
      tipo: 'whatsapp_producto'
    })
  } catch (error) {
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
