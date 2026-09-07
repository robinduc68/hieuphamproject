<template>
  <div class="admin-wrap">

    <!-- ── Sidebar ── -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">RBD</span>
        <div>
          <div class="logo-name">Robin Admin</div>
          <div class="logo-sub">Quản trị hệ thống</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item" :class="{ active: isActive(item) }">
          <span class="nav-icon" v-html="item.icon" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-bottom">
        <div class="user-row">
          <div class="user-avatar">{{ initials }}</div>
          <div class="user-info">
            <div class="user-name">{{ authStore.user?.full_name || authStore.user?.email }}</div>
            <div class="user-role">Administrator</div>
          </div>
        </div>
        <button class="logout-btn" @click="logout">
          <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M13 15l4-5-4-5"/><path d="M17 10H7"/><path d="M7 3H4a1 1 0 00-1 1v12a1 1 0 001 1h3"/></svg>
        </button>
      </div>
    </aside>

    <!-- ── Main ── -->
    <div class="main-wrap">
      <header class="topbar">
        <div class="topbar-title">{{ pageTitle }}</div>
        <a :href="homeUrl" target="_blank" rel="noopener" class="btn btn-secondary btn-sm">
          Xem trang chủ ↗
        </a>
      </header>

      <main class="content">
        <RouterView />
      </main>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { siteUrl } from '@/utils/siteUrl.js'

const authStore = useAuthStore()
const route     = useRouter()
const router    = useRouter()
const currentRoute = useRoute()

const homeUrl = siteUrl('/')

const allNavItems = [
  { to: '/dashboard',  label: 'Dashboard', perm: 'dashboard.view',     icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="2" width="7" height="7" rx="1"/><rect x="11" y="2" width="7" height="7" rx="1"/><rect x="2" y="11" width="7" height="7" rx="1"/><rect x="11" y="11" width="7" height="7" rx="1"/></svg>' },
  { to: '/products',   label: 'Sản phẩm', perm: 'products.view',      icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 3h14l-1.5 9H4.5L3 3z"/><circle cx="8" cy="17" r="1"/><circle cx="14" cy="17" r="1"/><path d="M1 1h2l.5 2"/></svg>' },
  { to: '/orders',     label: 'Đơn hàng', perm: 'orders.view',      icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4h12a1 1 0 011 1v10a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1z"/><path d="M7 8h6M7 11h4"/></svg>' },
  { to: '/categories', label: 'Danh mục', perm: 'categories.view',      icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 5h14M3 10h10M3 15h6"/></svg>' },
  { to: '/roles',         label: 'Vai trò',      perm: 'roles.view', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 2l6 3v5c0 3.5-2.4 6.4-6 8-3.6-1.6-6-4.5-6-8V5l6-3z"/><path d="M7.5 10l1.8 1.8L13 8"/></svg>' },
  { to: '/users',         label: 'Người dùng',   perm: 'users.view', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10" cy="7" r="3"/><path d="M3 17a7 7 0 0114 0"/></svg>' },
  { to: '/customization', label: 'Tùy chỉnh', perm: 'customization.view',    icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10" cy="10" r="3"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.22 4.22l1.42 1.42M14.36 14.36l1.42 1.42M4.22 15.78l1.42-1.42M14.36 5.64l1.42-1.42"/></svg>' },
  { to: '/posts',         label: 'Tin tức', perm: 'posts.view',       icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 4h10a1 1 0 011 1v11H4a1 1 0 01-1-1V4z"/><path d="M14 8h2a1 1 0 011 1v6a1 1 0 01-1 1h-2"/><path d="M6 7h4M6 10h4M6 13h3"/></svg>' },
  { to: '/settings',      label: 'Nội dung web', perm: 'content.view', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="4" width="16" height="12" rx="2"/><path d="M8 8.5l4 2.5-4 2.5z"/></svg>' },
]

// Ẩn hẳn tab không có quyền — router cũng chặn khi gõ thẳng URL
const navItems = computed(() => allNavItems.filter(i => !i.perm || authStore.can(i.perm)))

const pageTitles = {
  dashboard:     'Dashboard',
  products:      'Sản phẩm',
  'product-new':   'Thêm sản phẩm',
  'product-edit':  'Chỉnh sửa sản phẩm',
  orders:        'Đơn hàng',
  categories:    'Danh mục',
  users:         'Người dùng',
  roles:         'Vai trò & phân quyền',
  'no-access':     'Không có quyền',
  customization: 'Tùy chỉnh sản phẩm',
  posts:         'Tin tức',
  'post-new':      'Viết bài mới',
  'post-edit':     'Chỉnh sửa bài viết',
  settings:      'Nội dung website',
}

const pageTitle = computed(() => pageTitles[currentRoute.name] || 'Admin')
const initials  = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.email || 'A'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

function isActive(item) {
  return currentRoute.path.startsWith(item.to)
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-wrap {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,.07);
}
.logo-icon {
  width: 36px; height: 36px;
  background: var(--brand);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #fff;
  flex-shrink: 0;
}
.logo-name { font-size: 14px; font-weight: 600; color: #fff; }
.logo-sub  { font-size: 11px; color: rgba(255,255,255,.4); margin-top: 1px; }

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--sidebar-text);
  transition: all var(--trans);
  text-decoration: none;
}
.nav-item:hover { background: rgba(255,255,255,.07); color: #fff; }
.nav-item.active { background: var(--sidebar-active); color: #fff; }

.nav-icon { width: 18px; height: 18px; flex-shrink: 0; display: flex; }
.nav-icon :deep(svg) { width: 18px; height: 18px; }

.sidebar-bottom {
  padding: 12px 8px;
  border-top: 1px solid rgba(255,255,255,.07);
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}
.user-avatar {
  width: 32px; height: 32px;
  background: var(--brand);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: #fff;
  flex-shrink: 0;
}
.user-info { min-width: 0; }
.user-name { font-size: 12px; font-weight: 600; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: rgba(255,255,255,.4); }

.logout-btn {
  background: none;
  border: none;
  color: rgba(255,255,255,.4);
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all var(--trans);
  display: flex;
  flex-shrink: 0;
}
.logout-btn svg { width: 16px; height: 16px; }
.logout-btn:hover { background: rgba(255,255,255,.07); color: #fff; }

/* Main */
.main-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  height: var(--topbar-h);
  background: #fff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
}
.topbar-title { font-size: 16px; font-weight: 600; }

.content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
</style>
