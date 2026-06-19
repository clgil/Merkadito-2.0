import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useOfflineStore = defineStore('offline', () => {
  // Estado
  const isOnline = ref(navigator.onLine)
  const isSyncing = ref(false)
  const lastSyncTime = ref(null)
  const pendingActions = ref([])

  // Getters
  const offlineMode = computed(() => !isOnline.value)
  const hasPendingSync = computed(() => pendingActions.value.length > 0)

  // Acciones
  function setOnline(status) {
    isOnline.value = status
    if (status) {
      syncPendingActions()
    }
  }

  function addPendingAction(action) {
    pendingActions.value.push(action)
  }

  function removePendingAction(id) {
    pendingActions.value = pendingActions.value.filter(a => a.id !== id)
  }

  function setLastSyncTime(time) {
    lastSyncTime.value = time
  }

  async function syncPendingActions() {
    if (isSyncing.value || !isOnline.value) return
    
    isSyncing.value = true
    
    try {
      // Importar funciones de sincronización
      const { executeSync } = await import('../pwa/sync')
      await executeSync(pendingActions.value)
      pendingActions.value = []
      lastSyncTime.value = new Date().toISOString()
    } catch (error) {
      console.error('Error en sincronización:', error)
    } finally {
      isSyncing.value = false
    }
  }

  // Escuchar eventos de conexión
  if (typeof window !== 'undefined') {
    window.addEventListener('online', () => setOnline(true))
    window.addEventListener('offline', () => setOnline(false))
  }

  return {
    isOnline,
    isSyncing,
    lastSyncTime,
    pendingActions,
    offlineMode,
    hasPendingSync,
    setOnline,
    addPendingAction,
    removePendingAction,
    setLastSyncTime,
    syncPendingActions
  }
})
