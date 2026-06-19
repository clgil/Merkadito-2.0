import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Inicio' }
  },
  {
    path: '/buscar',
    name: 'Search',
    component: () => import('@/views/SearchView.vue'),
    meta: { title: 'Buscar' }
  },
  {
    path: '/empresa/:slug',
    name: 'Empresa',
    component: () => import('@/views/EmpresaView.vue'),
    meta: { title: 'Empresa' }
  },
  {
    path: '/producto/:id',
    name: 'Producto',
    component: () => import('@/views/ProductoView.vue'),
    meta: { title: 'Producto' }
  },
  {
    path: '/favoritos',
    name: 'Favoritos',
    component: () => import('@/views/FavoritosView.vue'),
    meta: { title: 'Favoritos' }
  },
  {
    path: '/offline',
    name: 'Offline',
    component: () => import('@/views/OfflineView.vue'),
    meta: { title: 'Sin conexión' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Actualizar título de página
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'Tu Merkadito'} - Directorio Comercial de Cuba`
  next()
})

export default router
