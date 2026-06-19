import { getPendingSyncActions, markSyncComplete } from './db'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export async function executeSync(actions) {
  if (!actions || actions.length === 0) return
  
  const results = []
  
  for (const action of actions) {
    try {
      let response
      
      switch (action.tipo) {
        case 'CREATE_EMPRESA':
          response = await axios.post(`${API_BASE_URL}/empresas/`, action.data)
          break
          
        case 'UPDATE_EMPRESA':
          response = await axios.put(
            `${API_BASE_URL}/empresas/${action.data.id}/`, 
            action.data
          )
          break
          
        case 'CREATE_PRODUCTO':
          response = await axios.post(`${API_BASE_URL}/productos/`, action.data)
          break
          
        case 'DELETE_PRODUCTO':
          response = await axios.delete(
            `${API_BASE_URL}/productos/${action.data.id}/`
          )
          break
          
        case 'ANALYTICS_CLICK':
          response = await axios.post(
            `${API_BASE_URL}/analytics/click/`, 
            action.data
          )
          break
          
        default:
          console.warn(`Tipo de acción desconocido: ${action.tipo}`)
          continue
      }
      
      if (response.status >= 200 && response.status < 300) {
        await markSyncComplete(action.id)
        results.push({ success: true, action })
      } else {
        results.push({ success: false, action, error: 'Status no exitoso' })
      }
    } catch (error) {
      console.error('Error sincronizando acción:', action, error)
      
      // Incrementar intentos
      if (action.intentos < 3) {
        action.intentos += 1
      } else {
        // Marcar como fallida después de 3 intentos
        await markSyncComplete(action.id)
      }
      
      results.push({ success: false, action, error: error.message })
    }
  }
  
  return results
}

// Función para sincronizar datos frescos desde el servidor
export async function syncFreshData() {
  try {
    const [empresas, productos] = await Promise.all([
      axios.get(`${API_BASE_URL}/empresas/`),
      axios.get(`${API_BASE_URL}/productos/`)
    ])
    
    // Guardar en caché IndexedDB
    const { guardarEmpresa, guardarProducto } = await import('./db')
    
    for (const empresa of empresas.data.results || empresas.data) {
      await guardarEmpresa(empresa)
    }
    
    for (const producto of productos.data.results || productos.data) {
      await guardarProducto(producto)
    }
    
    return { success: true }
  } catch (error) {
    console.error('Error sincronizando datos frescos:', error)
    return { success: false, error: error.message }
  }
}
