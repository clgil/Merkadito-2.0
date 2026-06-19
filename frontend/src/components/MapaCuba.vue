<template>
  <div class="mapa-cuba-container">
    <!-- Controles de radio -->
    <div class="radio-control" v-if="mostrarControles">
      <label for="radio-slider">Radio: {{ radioKm }} km</label>
      <input
        id="radio-slider"
        type="range"
        min="1"
        max="50"
        :value="radioKm"
        @input="$emit('radio-cambiado', Number($event.target.value))"
        class="slider"
      />
    </div>

    <!-- Botón mi ubicación -->
    <button
      v-if="mostrarMiUbicacion"
      class="btn-mi-ubicacion"
      @click="obtenerMiUbicacion"
      title="Mi ubicación"
    >
      📍
    </button>

    <!-- Mapa -->
    <div ref="mapContainer" class="mapa"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  lat: { type: Number, default: 21.5 },
  lon: { type: Number, default: -80.0 },
  zoom: { type: Number, default: 7 },
  empresas: { type: Array, default: () => [] },
  radioKm: { type: Number, default: 5 },
  mostrarMiUbicacion: { type: Boolean, default: true },
  mostrarControles: { type: Boolean, default: true }
})

const emit = defineEmits(['empresa-click', 'ubicacion-actualizada', 'radio-cambiado'])

const mapContainer = ref(null)
let map = null
let markersLayer = null
let circleLayer = null

// Inicializar mapa
onMounted(() => {
  if (!mapContainer.value) return

  // Importar leaflet dinámicamente para mejor performance
  import('leaflet').then((L) => {
    // Crear mapa centrado en Cuba
    map = L.map(mapContainer.value).setView([props.lat, props.lon], props.zoom)

    // Capa OpenStreetMap (gratuita)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18,
      className: 'osm-tile'
    }).addTo(map)

    // Capa de marcadores
    markersLayer = L.layerGroup().addTo(map)

    // Círculo de radio
    if (props.radioKm > 0) {
      circleLayer = L.circle([props.lat, props.lon], {
        radius: props.radioKm * 1000,
        color: '#3b82f6',
        fillColor: '#3b82f6',
        fillOpacity: 0.1,
        weight: 1
      }).addTo(map)
    }

    // Añadir marcadores de empresas
    actualizarMarcadores()

    // Evento moveend para emitir ubicación actualizada
    map.on('moveend', () => {
      const center = map.getCenter()
      emit('ubicacion-actualizada', {
        lat: center.lat,
        lon: center.lng
      })
    })
  })
})

// Actualizar marcadores cuando cambian las empresas
watch(() => props.empresas, () => {
  actualizarMarcadores()
}, { deep: true })

// Actualizar círculo de radio
watch(() => props.radioKm, (newRadius) => {
  if (!map || !circleLayer) return
  
  const center = map.getCenter()
  circleLayer.setRadius(newRadius * 1000)
})

function actualizarMarcadores() {
  if (!markersLayer || !map) return

  markersLayer.clearLayers()

  props.empresas.forEach(empresa => {
    if (!empresa.latitud || !empresa.longitud) return

    // Icono personalizado
    const iconHtml = `
      <div class="marker-pin" style="background-color: ${empresa.color || '#ef4444'}">
        ${empresa.icono || '🏪'}
      </div>
    `

    const customIcon = L.divIcon({
      className: 'custom-marker',
      html: iconHtml,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -32]
    })

    const marker = L.marker([empresa.latitud, empresa.longitud], { icon: customIcon })
    
    // Popup con información
    const popupContent = `
      <div class="popup-empresa">
        <h3>${empresa.nombre}</h3>
        ${empresa.categoria ? `<p class="categoria">${empresa.categoria}</p>` : ''}
        ${empresa.direccion ? `<p class="direccion">📍 ${empresa.direccion}</p>` : ''}
        ${empresa.whatsapp ? `<a href="https://wa.me/${empresa.whatsapp}" target="_blank" class="btn-whatsapp">📲 Contactar</a>` : ''}
      </div>
    `

    marker.bindPopup(popupContent)

    // Click en marcador
    marker.on('click', () => {
      emit('empresa-click', { empresa, lat: empresa.latitud, lon: empresa.longitud })
    })

    markersLayer.addLayer(marker)
  })
}

// Obtener ubicación del usuario
function obtenerMiUbicacion() {
  if (!navigator.geolocation) {
    alert('Geolocalización no soportada en este navegador')
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      
      if (map) {
        map.setView([latitude, longitude], 13)
        emit('ubicacion-actualizada', { lat: latitude, lon: longitude })
        
        // Marcador de mi ubicación
        import('leaflet').then((L) => {
          L.circleMarker([latitude, longitude], {
            radius: 8,
            color: '#2563eb',
            fillColor: '#2563eb',
            fillOpacity: 0.5
          }).addTo(markersLayer)
        })
      }
    },
    (error) => {
      console.error('Error obteniendo ubicación:', error)
      alert('No se pudo obtener tu ubicación. Verifica los permisos.')
    }
  )
}

// Métodos públicos
defineExpose({
  centrarEn(lat, lon, zoomLevel) {
    if (map) {
      map.setView([lat, lon], zoomLevel || map.getZoom())
    }
  },
  
  mostrarTodas() {
    if (!map || props.empresas.length === 0) return
    
    const coords = props.empresas
      .filter(e => e.latitud && e.longitud)
      .map(e => [e.latitud, e.longitud])
    
    if (coords.length > 0) {
      const bounds = L.latLngBounds(coords)
      map.fitBounds(bounds, { padding: [50, 50] })
    }
  },
  
  limpiarMarcadores() {
    if (markersLayer) {
      markersLayer.clearLayers()
    }
  }
})
</script>

<style scoped>
.mapa-cuba-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.mapa {
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* Controles de radio */
.radio-control {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  z-index: 1000;
  font-size: 14px;
}

.slider {
  display: block;
  width: 150px;
  margin-top: 8px;
  accent-color: #3b82f6;
}

/* Botón mi ubicación */
.btn-mi-ubicacion {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e5e7eb;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  z-index: 1000;
  transition: all 0.2s;
}

.btn-mi-ubicacion:hover {
  background: #f3f4f6;
  transform: scale(1.05);
}

/* Marcador personalizado */
:deep(.custom-marker) {
  background: transparent;
  border: none;
}

.marker-pin {
  width: 32px;
  height: 32px;
  border-radius: 50% 50% 50% 0;
  background: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  transform: rotate(-45deg);
}

.marker-pin :first-child {
  transform: rotate(45deg);
}

/* Popup */
:deep(.popup-empresa) {
  min-width: 200px;
}

.popup-empresa h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #1f2937;
}

.popup-empresa .categoria {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 4px;
}

.popup-empresa .direccion {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 8px;
}

.btn-whatsapp {
  display: inline-block;
  background: #25D366;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-whatsapp:hover {
  background: #20bd5a;
}

/* Responsive */
@media (max-width: 640px) {
  .radio-control {
    top: auto;
    bottom: 80px;
    right: 10px;
    left: 10px;
  }
  
  .slider {
    width: 100%;
  }
  
  .btn-mi-ubicacion {
    bottom: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
}
</style>
