<template>
  <transition name="slide-down">
    <div v-if="showBanner" :class="['offline-banner', bannerClass]">
      <div class="banner-content">
        <span class="banner-icon">{{ icon }}</span>
        <span class="banner-text">{{ message }}</span>
      </div>
      <button v-if="canRetry" @click="onRetry" class="retry-btn">
        Reintentar
      </button>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useOfflineStore } from '@/stores/offline'

const props = defineProps({
  customMessage: String
})

const emit = defineEmits(['retry'])

const offlineStore = useOfflineStore()

const showBanner = computed(() => {
  return offlineStore.offlineMode || offlineStore.isSyncing
})

const bannerClass = computed(() => {
  if (offlineStore.isSyncing) return 'syncing'
  if (offlineStore.offlineMode) return 'offline'
  return ''
})

const icon = computed(() => {
  if (offlineStore.isSyncing) return '🔄'
  if (offlineStore.offlineMode) return '📴'
  return '✅'
})

const message = computed(() => {
  if (props.customMessage) return props.customMessage
  if (offlineStore.isSyncing) return 'Sincronizando datos...'
  if (offlineStore.offlineMode) return 'Estás offline. Mostrando datos en caché.'
  return 'Conexión restaurada'
})

const canRetry = computed(() => {
  return offlineStore.offlineMode && offlineStore.hasPendingSync
})

function onRetry() {
  emit('retry')
}
</script>

<style scoped>
.offline-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 9999;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.offline {
  background-color: #fef3c7;
  color: #92400e;
}

.syncing {
  background-color: #dbeafe;
  color: #1e40af;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.retry-btn {
  padding: 0.25rem 0.75rem;
  background-color: rgba(0,0,0,0.1);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background-color: rgba(0,0,0,0.15);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
