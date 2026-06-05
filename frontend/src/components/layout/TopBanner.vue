<template>
  <nav class="top-banner">
    <ul class="top-nav">
      <li v-for="item in navItems" :key="item.label">
        <RouterLink :to="item.to" class="top-link">{{ item.label }}</RouterLink>
      </li>
    </ul>
  </nav>
</template>

<script setup>
const navItems = [
  { label: 'Trang chủ',          to: '/' },
  { label: 'Lựa chọn menu',      to: '/lua-chon-menu' },
  { label: 'Từng sản phẩm',      to: '/cua-hang' },
  { label: 'Trang chọn vải',     to: '/chon-vai' },
  { label: 'Câu hỏi thường gặp', to: '/faq' },
  { label: 'Tin tức',            to: '/tin-tuc' },
  { label: 'Thanh toán',         to: '/thanh-toan' },
]
</script>

<style scoped>
.top-banner {
  display: block;
  width: 100%;
  background: var(--bg-white);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 1001;
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0;
  list-style: none;
  width: 100%;
  padding: 8px 48px;
}

.top-nav li + li::before {
  content: '|';
  margin: 0 14px;
  color: var(--border);
  font-size: 11px;
}

.top-link {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2px;
  color: var(--text-medium);
  transition: color var(--transition);
  white-space: nowrap;
}

.top-link:hover { color: var(--text-dark); }

.router-link-active {
  color: var(--text-dark);
  font-weight: 700;
}
</style>
