<template>
  <header class="app-header" :class="{ 'app-header--overlay': overlay }">
    <div class="header-wrap">

      <!-- Nav card — bo góc -->
      <div class="header-card">

        <!-- Logo -->
        <LogoBrand size="sm" class="logo-block" />

        <!-- Nav -->
        <nav class="main-nav">
          <RouterLink to="/ve-chung-toi" class="nav-link">Về chúng tôi</RouterLink>

          <!-- Sản phẩm + dropdown -->
          <div
            class="nav-dropdown-wrap"
            @mouseenter="menuOpen = true"
            @mouseleave="menuOpen = false"
          >
            <!-- Click = về trang shop không filter; hover vẫn mở mega menu -->
            <RouterLink
              to="/cua-hang"
              class="nav-link"
              :class="{ 'nav-link--open': menuOpen }"
              @click="menuOpen = false"
            >Sản phẩm</RouterLink>
            <MegaMenu
              :open="menuOpen"
              :categories="categories"
              @close="menuOpen = false"
              @keep="menuOpen = true"
            />
          </div>

          <RouterLink to="/faq"     class="nav-link">Câu hỏi thường gặp</RouterLink>
          <RouterLink to="/tin-tuc" class="nav-link">Tin tức</RouterLink>
        </nav>

        <!-- Icons -->
        <div class="header-icons">
          <button class="icon-btn" @click="searchOpen = !searchOpen" aria-label="Tìm kiếm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/>
            </svg>
          </button>

          <RouterLink to="/tai-khoan" class="icon-btn" aria-label="Tài khoản">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </RouterLink>

          <div class="lang-btn">
            <span class="flag">🇻🇳</span>
            <span class="lang-text">VI</span>
            <svg viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" class="chevron">
              <path d="M1 1l4 4 4-4"/>
            </svg>
          </div>

          <button class="icon-btn cart-btn" @click="cartOpen = true" aria-label="Giỏ hàng">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <path d="M16 10a4 4 0 01-8 0"/>
            </svg>
            <span v-if="cartStore.count > 0" class="cart-badge">{{ cartStore.count }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Search bar -->
    <Transition name="search-bar">
      <div v-if="searchOpen" class="search-bar">
        <div class="search-inner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="search-icon">
            <circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/>
          </svg>
          <input ref="searchInput" v-model="searchQuery" type="text"
            class="search-input" placeholder="Tìm kiếm sản phẩm…" @keyup.enter="doSearch" />
          <button class="search-close" @click="searchOpen = false">✕</button>
        </div>
      </div>
    </Transition>

    <CartDrawer :open="cartOpen" @close="cartOpen = false" />
  </header>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import CartDrawer from '@/components/ui/CartDrawer.vue'
import MegaMenu  from '@/components/layout/MegaMenu.vue'
import LogoBrand  from '@/components/ui/LogoBrand.vue'
import { useCartStore }  from '@/stores/cart'
import { useCategories } from '@/composables/useCategories'

const props = defineProps({
  overlay: { type: Boolean, default: false },
})

const menuOpen = ref(false)

// Menu danh mục lấy thẳng từ API — admin thêm/sửa danh mục là menu đổi theo
const { categories } = useCategories()

const cartStore   = useCartStore()
const router      = useRouter()
const cartOpen    = ref(false)
const searchOpen  = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)

function doSearch() {
  if (!searchQuery.value.trim()) return
  router.push({ path: '/cua-hang', query: { search: searchQuery.value } })
  searchOpen.value  = false
  searchQuery.value = ''
}

watch(searchOpen, async (val) => { if (val) { await nextTick(); searchInput.value?.focus() } })
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 999;
  background: var(--bg-white);
  border-bottom: 1px solid var(--border);
}

/* Trang chủ: đè lên video */
.app-header--overlay {
  position: absolute;
  top: 0; left: 0; right: 0;
  background: transparent;
  border-bottom: none;
}

/* Outer wrapper: badge + card side by side */
.header-wrap {
  display: flex;
  align-items: center;
  padding: 6px 16px 6px 6px;
  max-width: 1440px;
  margin: 0 auto;
  gap: 8px;
}


/* Rounded card — stretch so nav links fill full height */
.header-card {
  flex: 1;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: stretch;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 10px;
  height: 62px;
  background: var(--bg-white);
}

/* Logo */
.logo-block {
  padding: 4px 20px 4px 24px;
  justify-content: center;
}

/* Nav — stretch links to full card height */
.main-nav {
  display: flex;
  align-items: stretch;
  justify-content: center;
}

.nav-dropdown-wrap {
  position: relative;
  display: flex;
  align-items: stretch;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0 22px;
  font-size: 18px;
  font-weight: 400;
  color: var(--text-dark);
  white-space: nowrap;
  transition: background var(--transition), color var(--transition);
  height: 100%;
  border: none;
  background: none;
  cursor: pointer;
  font-family: var(--font-body);
}
.nav-link:hover,
.nav-link--open {
  background: var(--brand-red);
  color: #fff;
}

/* Icons */
.header-icons {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
}
.icon-btn {
  background: none;
  border: none;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  padding: 5px;
  cursor: pointer;
  position: relative;
  transition: color var(--transition);
}
.icon-btn:hover { color: var(--brand-red); }
.icon-btn svg { width: 20px; height: 20px; }

.lang-btn {
  display: flex;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-dark);
  padding: 5px;
  transition: color var(--transition);
}
.lang-btn:hover { color: var(--brand-red); }
.flag { font-size: 14px; }
.chevron { width: 8px; height: 8px; }

.cart-btn { position: relative; }
.cart-badge {
  position: absolute;
  top: 0; right: 0;
  background: var(--brand-red);
  color: white;
  font-size: 9px;
  font-weight: 600;
  width: 15px; height: 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Search */
.search-bar {
  border-top: 1px solid var(--border);
  background: var(--bg-white);
}
.search-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 40px;
  max-width: 1440px;
  margin: 0 auto;
}
.search-icon { width: 18px; height: 18px; color: var(--text-light); flex-shrink: 0; }
.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  outline: none;
}
.search-input::placeholder { color: var(--text-light); }
.search-close {
  background: none;
  border: none;
  font-size: 14px;
  color: var(--text-light);
  cursor: pointer;
  transition: color var(--transition);
}
.search-close:hover { color: var(--text-dark); }
.search-bar-enter-active,
.search-bar-leave-active { transition: max-height .3s ease, opacity .3s ease; overflow: hidden; max-height: 60px; }
.search-bar-enter-from,
.search-bar-leave-to { max-height: 0; opacity: 0; }
</style>
