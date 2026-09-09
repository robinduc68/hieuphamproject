<template>
  <header class="app-header" :class="{ 'app-header--overlay': overlay }">
    <div class="header-wrap">

      <!-- Nav card — bo góc -->
      <div class="header-card">

        <!-- Mở menu trên mobile -->
        <button class="burger-btn" aria-label="Mở menu" @click="mobileOpen = true">
          <span /><span /><span />
        </button>

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

    <!-- ── Menu mobile ───────────────────────────────────────────────── -->
    <Transition name="mnav-fade">
      <div v-if="mobileOpen" class="mnav-overlay" @click="mobileOpen = false" />
    </Transition>
    <Transition name="mnav-slide">
      <nav v-if="mobileOpen" class="mnav" aria-label="Menu">
        <div class="mnav-head">
          <LogoBrand size="sm" />
          <button class="mnav-close" aria-label="Đóng menu" @click="mobileOpen = false">✕</button>
        </div>

        <div class="mnav-body">
          <RouterLink to="/ve-chung-toi" class="mnav-link" @click="mobileOpen = false">Về chúng tôi</RouterLink>

          <!-- Sản phẩm: bấm mũi tên để mở danh mục, bấm chữ để vào trang shop -->
          <div class="mnav-group">
            <div class="mnav-link mnav-link--row">
              <RouterLink to="/cua-hang" class="mnav-link-text" @click="mobileOpen = false">Sản phẩm</RouterLink>
              <button
                class="mnav-toggle"
                :class="{ open: mobileCatsOpen }"
                :aria-expanded="mobileCatsOpen"
                aria-label="Mở danh mục"
                @click="mobileCatsOpen = !mobileCatsOpen"
              >
                <svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 1l5 5 5-5"/></svg>
              </button>
            </div>

            <div v-if="mobileCatsOpen" class="mnav-sub">
              <template v-for="cat in categories" :key="cat.id">
                <RouterLink
                  :to="`/cua-hang?category=${cat.slug}`"
                  class="mnav-sub-link mnav-sub-link--parent"
                  @click="mobileOpen = false"
                >{{ cat.name }}</RouterLink>
                <RouterLink
                  v-for="sub in cat.subcategories"
                  :key="sub.id"
                  :to="`/cua-hang?category=${cat.slug}&subcategory=${sub.slug}`"
                  class="mnav-sub-link"
                  @click="mobileOpen = false"
                >{{ sub.name }}</RouterLink>
              </template>
            </div>
          </div>

          <RouterLink to="/faq"        class="mnav-link" @click="mobileOpen = false">Câu hỏi thường gặp</RouterLink>
          <RouterLink to="/tin-tuc"    class="mnav-link" @click="mobileOpen = false">Tin tức</RouterLink>
          <RouterLink to="/tai-khoan"  class="mnav-link" @click="mobileOpen = false">Tài khoản</RouterLink>
        </div>

        <div class="mnav-foot">
          <span class="flag">🇻🇳</span> VI
        </div>
      </nav>
    </Transition>

    <CartDrawer :open="cartOpen" @close="cartOpen = false" />
  </header>
</template>

<script setup>
import { ref, nextTick, watch, onUnmounted } from 'vue'
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

// Menu mobile (drawer trượt từ trái)
const mobileOpen     = ref(false)
const mobileCatsOpen = ref(false)

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

// Không cho trang phía sau cuộn khi drawer đang mở
watch(mobileOpen, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})

// Đổi trang thì đóng menu (bấm link trong drawer hoặc nút back)
watch(() => router.currentRoute.value.fullPath, () => {
  mobileOpen.value = false
})

onUnmounted(() => { document.body.style.overflow = '' })
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

/* ══ Mobile ═══════════════════════════════════════════════════════════ */

/* Nút hamburger — chỉ hiện trên mobile */
.burger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 44px;
  border: none;
  background: none;
  padding: 0 0 0 14px;
}
.burger-btn span {
  display: block;
  width: 20px; height: 1.6px;
  background: var(--text-dark);
  border-radius: 2px;
}
.app-header--overlay .burger-btn span { background: var(--text-dark); }

/* Drawer */
.mnav-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.42);
  z-index: 1000;
}
.mnav {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: min(84vw, 340px);
  background: var(--bg-white);
  z-index: 1001;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 30px rgba(0,0,0,.16);
}
.mnav-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.mnav-close {
  background: none; border: none;
  font-size: 17px; color: var(--text-medium);
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
}
.mnav-body {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 6px 0 20px;
}
.mnav-link {
  display: flex; align-items: center;
  min-height: 52px;
  padding: 0 18px;
  font-family: var(--font-body);
  font-size: 17px;
  color: var(--text-dark);
  border-bottom: 1px solid #F0EFEC;
}
.mnav-link--row { padding-right: 6px; justify-content: space-between; gap: 8px; }
.mnav-link-text { flex: 1; padding: 14px 0; }
.mnav-toggle {
  width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
  background: none; border: none; color: var(--text-medium);
  flex-shrink: 0;
}
.mnav-toggle svg { width: 12px; height: 8px; transition: transform var(--transition); }
.mnav-toggle.open svg { transform: rotate(180deg); }

.mnav-sub { background: #FBFAF7; border-bottom: 1px solid #F0EFEC; }
.mnav-sub-link {
  display: block;
  padding: 12px 18px 12px 32px;
  font-size: 15px;
  color: var(--text-medium);
}
.mnav-sub-link--parent {
  padding-left: 26px;
  color: var(--brand-red);
  font-weight: 600;
}

.mnav-foot {
  flex-shrink: 0;
  padding: 14px 18px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-medium);
  display: flex; align-items: center; gap: 6px;
}

.mnav-fade-enter-active, .mnav-fade-leave-active { transition: opacity .25s ease; }
.mnav-fade-enter-from,   .mnav-fade-leave-to     { opacity: 0; }
.mnav-slide-enter-active, .mnav-slide-leave-active { transition: transform .28s cubic-bezier(.25,.46,.45,.94); }
.mnav-slide-enter-from,   .mnav-slide-leave-to     { transform: translateX(-100%); }

/* Tablet ngang: nav chữ to quá thì thu lại */
@media (max-width: 1100px) {
  .nav-link   { padding: 0 14px; font-size: 16px; }
  .logo-block { padding: 4px 12px 4px 16px; }
  .header-icons { gap: 8px; padding: 0 14px; }
}

/* Từ tablet dọc trở xuống: ẩn nav ngang, dùng drawer */
@media (max-width: 900px) {
  .burger-btn { display: flex; }
  .main-nav   { display: none; }
  .header-wrap  { padding: 6px 10px 6px 4px; gap: 6px; }
  .header-card  { grid-template-columns: auto 1fr auto; height: 56px; }
  .logo-block   { padding: 4px 6px; justify-content: flex-start; }
  .header-icons { padding: 0 12px 0 0; gap: 2px; }
  .lang-btn     { display: none; }
  .search-inner { padding: 10px 16px; }
}

@media (max-width: 380px) {
  .header-icons .icon-btn[aria-label="Tài khoản"] { display: none; }
}
</style>
