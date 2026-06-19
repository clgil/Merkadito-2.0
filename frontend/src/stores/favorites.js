import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { obtenerFavoritos, toggleFavorito as toggleFavoritoDB } from '../pwa/db'

export const useFavoritesStore = defineStore('favorites', () => {
  // Estado
  const favorites = ref([])
  const loading = ref(false)

  // Getters
  const favoriteIds = computed(() => favorites.value.map(f => f.id))
  const count = computed(() => favorites.value.length)

  // Acciones
  async function loadFavorites() {
    loading.value = true
    try {
      favorites.value = await obtenerFavoritos()
    } catch (error) {
      console.error('Error cargando favoritos:', error)
    } finally {
      loading.value = false
    }
  }

  async function toggleFavorite(item) {
    const isFavorite = favoriteIds.value.includes(item.id)
    
    try {
      const added = await toggleFavoritoDB(item)
      
      if (added) {
        favorites.value.push({ ...item, _added_at: Date.now() })
      } else {
        favorites.value = favorites.value.filter(f => f.id !== item.id)
      }
      
      return added
    } catch (error) {
      console.error('Error toggling favorite:', error)
      return null
    }
  }

  function isFavorite(id) {
    return favoriteIds.value.includes(id)
  }

  function removeFavorite(id) {
    favorites.value = favorites.value.filter(f => f.id !== id)
  }

  return {
    favorites,
    loading,
    favoriteIds,
    count,
    loadFavorites,
    toggleFavorite,
    isFavorite,
    removeFavorite
  }
})
