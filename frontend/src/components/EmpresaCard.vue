<template>
  <div class="bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition">
    <router-link :to="`/empresa/${empresa.slug}`" class="block">
      <div class="p-4">
        <div class="flex items-start gap-3">
          <!-- Logo -->
          <div class="w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
            <img
              v-if="empresa.logo"
              :src="empresa.logo"
              :alt="empresa.nombre"
              loading="lazy"
              class="w-full h-full object-cover rounded-lg"
            />
            <span v-else>🏪</span>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 truncate">
              {{ empresa.nombre }}
            </h3>
            <p class="text-sm text-gray-600 mt-1">
              {{ empresa.categoria }}
            </p>
            <p class="text-xs text-gray-500 mt-1 flex items-center gap-1">
              📍 {{ empresa.municipio }}, {{ empresa.provincia }}
            </p>
          </div>
        </div>

        <!-- Estado y WhatsApp -->
        <div class="mt-3 flex items-center justify-between">
          <span
            :class="[
              'text-xs px-2 py-1 rounded-full',
              empresa.activo ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            ]"
          >
            {{ empresa.activo ? '✅ Abierto' : '⏸ Cerrado' }}
          </span>
          
          <a
            :href="whatsappLink"
            target="_blank"
            rel="noopener noreferrer"
            class="text-xs bg-green-500 text-white px-3 py-1.5 rounded-full hover:bg-green-600 transition flex items-center gap-1"
            @click.stop="registrarClick"
          >
            📲 WhatsApp
          </a>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import axios from 'axios'

const props = defineProps({
  empresa: {
    type: Object,
    required: true
  }
})

const whatsappLink = computed(() => {
  const numero = props.empresa.whatsapp || ''
  const mensaje = `Hola, vi tu negocio en Tu Merkadito`
  const numeroLimpio = numero.replace('+', '').replace(' ', '').replace('-', '')
  return `https://wa.me/${numeroLimpio}?text=${encodeURIComponent(mensaje)}`
})

async function registrarClick() {
  try {
    await axios.post('/api/v1/analytics/click/', {
      empresa_id: props.empresa.id,
      tipo: 'whatsapp_empresa'
    })
  } catch (error) {
    console.log('Click registrado offline')
  }
}
</script>
