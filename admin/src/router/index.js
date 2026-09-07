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
      { path: 'dashboard',  name: 'dashboard',  component: () => import('@/views/DashboardView.vue'), meta: { perm: 'dashboard.view' } },
      { path: 'products',   name: 'products',   component: () => import('@/views/ProductsView.vue'),  meta: { perm: 'products.view' } },
      { path: 'products/new',       name: 'product-new',  component: () => import('@/views/ProductFormView.vue'), meta: { perm: 'products.create' } },
      { path: 'products/:id/edit',  name: 'product-edit', component: () => import('@/views/ProductFormView.vue'), meta: { perm: 'products.update' } },
      { path: 'posts',      name: 'posts',      component: () => import('@/views/PostsView.vue'), meta: { perm: 'posts.view' } },
      { path: 'posts/new',      name: 'post-new',  component: () => import('@/views/PostFormView.vue'), meta: { perm: 'posts.create' } },
      { path: 'posts/:id/edit', name: 'post-edit', component: () => import('@/views/PostFormView.vue'), meta: { perm: 'posts.update' } },
      { path: 'orders',        name: 'orders',        component: () => import('@/views/OrdersView.vue'),        meta: { perm: 'orders.view' } },
      { path: 'categories',    name: 'categories',    component: () => import('@/views/CategoriesView.vue'),    meta: { perm: 'categories.view' } },
      { path: 'users',         name: 'users',         component: () => import('@/views/UsersView.vue'),         meta: { perm: 'users.view' } },
      { path: 'roles',         name: 'roles',         component: () => import('@/views/RolesView.vue'),         meta: { perm: 'roles.view' } },
      { path: 'customization', name: 'customization', component: () => import('@/views/CustomizationView.vue'), meta: { perm: 'customization.view' } },
      { path: 'settings',      name: 'settings',      component: () => import('@/views/SettingsView.vue'),      meta: { perm: 'content.view' } },
      { path: 'no-access',     name: 'no-access',     component: () => import('@/views/NoAccessView.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// Trang đầu tiên tài khoản này được vào — dùng khi họ không có quyền xem
// Dashboard (VD nhân viên nội dung thì mở thẳng Sản phẩm).
export function firstAllowedPath(auth) {
  const order = [
    ['dashboard.view',     '/dashboard'],
    ['products.view',      '/products'],
    ['orders.view',        '/orders'],
    ['posts.view',         '/posts'],
    ['categories.view',    '/categories'],
    ['content.view',       '/settings'],
    ['customization.view', '/customization'],
    ['users.view',         '/users'],
    ['roles.view',         '/roles'],
  ]
  for (const [perm, path] of order) if (auth.can(perm)) return path
  return null
}

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAdmin && !auth.isLoggedIn) return '/login'
  if (to.path === '/login' && auth.isLoggedIn) return firstAllowedPath(auth) || '/no-access'

  // Chặn cả khi gõ thẳng URL — server vẫn chặn lần nữa ở API.
  const perm = to.meta?.perm
  if (perm && auth.isLoggedIn && !auth.can(perm)) {
    const fallback = firstAllowedPath(auth)
    return fallback && fallback !== to.path ? fallback : '/no-access'
  }
})

export default router
