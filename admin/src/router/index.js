import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  { path: '/login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('@/components/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: '',         redirect: '/dashboard' },
      { path: 'dashboard',  name: 'dashboard',  component: () => import('@/views/DashboardView.vue') },
      { path: 'products',   name: 'products',   component: () => import('@/views/ProductsView.vue') },
      { path: 'products/new',       name: 'product-new',  component: () => import('@/views/ProductFormView.vue') },
      { path: 'products/:id/edit',  name: 'product-edit', component: () => import('@/views/ProductFormView.vue') },
      { path: 'posts',      name: 'posts',      component: () => import('@/views/PostsView.vue') },
      { path: 'posts/new',      name: 'post-new',  component: () => import('@/views/PostFormView.vue') },
      { path: 'posts/:id/edit', name: 'post-edit', component: () => import('@/views/PostFormView.vue') },
      { path: 'orders',        name: 'orders',        component: () => import('@/views/OrdersView.vue') },
      { path: 'categories',    name: 'categories',    component: () => import('@/views/CategoriesView.vue') },
      { path: 'users',         name: 'users',         component: () => import('@/views/UsersView.vue') },
      { path: 'customization', name: 'customization', component: () => import('@/views/CustomizationView.vue') },
      { path: 'settings',      name: 'settings',      component: () => import('@/views/SettingsView.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAdmin && !auth.isLoggedIn) return '/login'
  if (to.path === '/login' && auth.isLoggedIn) return '/dashboard'
})

export default router
