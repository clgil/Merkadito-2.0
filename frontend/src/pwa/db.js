import { openDB } from 'idb'

const DB_NAME = 'tu-merkadito-db'
const DB_VERSION = 1

export async function initDB() {
  return await openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      // Store para empresas
      if (!db.objectStoreNames.contains('empresas')) {
        db.createObjectStore('empresas', { keyPath: 'id' })
      }
      
      // Store para productos
      if (!db.objectStoreNames.contains('productos')) {
        db.createObjectStore('productos', { keyPath: 'id' })
      }
      
      // Store para búsquedas recientes
      if (!db.objectStoreNames.contains('busquedas')) {
        const store = db.createObjectStore('busquedas', { 
          keyPath: 'id', 
          autoIncrement: true 
        })
        store.createIndex('termino', 'termino')
        store.createIndex('fecha', 'fecha')
      }
      
      // Store para favoritos
      if (!db.objectStoreNames.contains('favoritos')) {
        db.createObjectStore('favoritos', { keyPath: 'id' })
      }
      
      // Store para cola de sincronización
      if (!db.objectStoreNames.contains('syncQueue')) {
        const store = db.createObjectStore('syncQueue', { 
          keyPath: 'id', 
          autoIncrement: true 
        })
        store.createIndex('tipo', 'tipo')
        store.createIndex('pendiente', 'pendiente')
      }
    }
  })
}

// Operaciones CRUD genéricas
export async function dbGet(storeName, key) {
  const db = await initDB()
  return await db.get(storeName, key)
}

export async function dbGetAll(storeName) {
  const db = await initDB()
  return await db.getAll(storeName)
}

export async function dbPut(storeName, item) {
  const db = await initDB()
  return await db.put(storeName, item)
}

export async function dbDelete(storeName, key) {
  const db = await initDB()
  return await db.delete(storeName, key)
}

export async function dbClear(storeName) {
  const db = await initDB()
  return await db.clear(storeName)
}

// Métodos específicos para empresas
export async function guardarEmpresa(empresa) {
  return await dbPut('empresas', {
    ...empresa,
    _cached_at: Date.now()
  })
}

export async function obtenerEmpresa(id) {
  return await dbGet('empresas', id)
}

export async function obtenerTodasLasEmpresas() {
  return await dbGetAll('empresas')
}

// Métodos específicos para productos
export async function guardarProducto(producto) {
  return await dbPut('productos', {
    ...producto,
    _cached_at: Date.now()
  })
}

export async function obtenerProductosPorEmpresa(empresaId) {
  const db = await initDB()
  const productos = await db.getAll('productos')
  return productos.filter(p => p.empresa_id === empresaId)
}

// Métodos para búsquedas recientes
export async function guardarBusqueda(termino, resultados = []) {
  const db = await initDB()
  return await db.put('busquedas', {
    termino,
    resultados: resultados.length,
    fecha: new Date().toISOString()
  })
}

export async function obtenerBusquedasRecientes(limit = 10) {
  const db = await initDB()
  const busquedas = await db.getAll('busquedas')
  return busquedas
    .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
    .slice(0, limit)
}

// Métodos para favoritos
export async function toggleFavorito(item) {
  const existente = await dbGet('favoritos', item.id)
  if (existente) {
    await dbDelete('favoritos', item.id)
    return false
  } else {
    await dbPut('favoritos', {
      ...item,
      _added_at: Date.now()
    })
    return true
  }
}

export async function obtenerFavoritos() {
  return await dbGetAll('favoritos')
}

export async function esFavorito(id) {
  const item = await dbGet('favoritos', id)
  return !!item
}

// Cola de sincronización
export async function addToSyncQueue(action) {
  const db = await initDB()
  return await db.put('syncQueue', {
    ...action,
    pendiente: true,
    intentos: 0,
    creado_en: Date.now()
  })
}

export async function getPendingSyncActions() {
  const db = await initDB()
  const actions = await db.getAll('syncQueue')
  return actions.filter(a => a.pendiente)
}

export async function markSyncComplete(id) {
  const db = await initDB()
  await db.delete('syncQueue', id)
}
