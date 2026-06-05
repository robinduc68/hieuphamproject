<template>
  <div class="shop-page">

    <!-- Page header -->
    <div class="shop-hero">
      <span class="section-label">Cửa Hàng</span>
      <h1 class="shop-title">Tất Cả Sản Phẩm</h1>
      <p class="shop-sub">{{ total }} thiết kế</p>
    </div>

    <div class="shop-layout">
      <!-- ── Sidebar filter ─────────────────────────────────────────── -->
      <aside class="shop-sidebar" :class="{ 'sidebar-open': sidebarOpen }">
        <div class="sidebar-header">
          <h2 class="sidebar-title">Bộ Lọc</h2>
          <button class="sidebar-close" @click="sidebarOpen = false" aria-label="Đóng bộ lọc">✕</button>
        </div>

        <!-- Search -->
        <div class="filter-group">
          <label class="filter-label">Tìm kiếm</label>
          <div class="search-wrap">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" class="search-icon">
              <circle cx="9" cy="9" r="6"/><path d="M15 15l3 3"/>
            </svg>
            <input
              v-model="searchInput"
              type="text"
              class="search-input"
              placeholder="Tên sản phẩm..."
              @keyup.enter="applySearch"
            />
          </div>
        </div>

        <!-- Category -->
        <div class="filter-group">
          <label class="filter-label">Danh Mục</label>
          <div class="filter-options">
            <button
              class="filter-chip"
              :class="{ active: !params.category }"
              @click="setCategory(null)"
            >Tất cả</button>
            <button
              v-for="cat in categories"
              :key="cat.id"
              class="filter-chip"
              :class="{ active: params.category === cat.slug }"
              @click="setCategory(cat.slug)"
            >{{ cat.name }}</button>
          </div>
        </div>

        <!-- Status filters -->
        <div class="filter-group">
          <label class="filter-label">Trạng Thái</label>
          <div class="filter-options">
            <button
              class="filter-chip"
              :class="{ active: params.is_new === true }"
              @click="toggleFilter('is_new', true)"
            >Mới nhất</button>
            <button
              class="filter-chip"
              :class="{ active: params.is_featured === true }"
              @click="toggleFilter('is_featured', true)"
            >Nổi bật</button>
          </div>
        </div>

        <!-- Reset -->
        <button class="reset-btn" @click="resetFilters">Xoá bộ lọc</button>
      </aside>

      <!-- ── Product area ───────────────────────────────────────────── -->
      <div class="shop-main">

        <!-- Toolbar -->
        <div class="shop-toolbar">
          <button class="filter-toggle-btn" @click="sidebarOpen = true" aria-label="Mở bộ lọc">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M3 5h14M6 10h8M9 15h2"/>
            </svg>
            Bộ lọc
          </button>

          <span class="toolbar-count">{{ total }} sản phẩm</span>

          <select v-model="sortBy" class="sort-select" @change="applySort">
            <option value="">Sắp xếp mặc định</option>
            <option value="newest">Mới nhất</option>
            <option value="price_asc">Giá tăng dần</option>
            <option value="price_desc">Giá giảm dần</option>
          </select>
        </div>

        <!-- Active filter tags -->
        <div v-if="hasActiveFilters" class="active-filters">
          <span v-if="params.search" class="filter-tag">
            "{{ params.search }}"
            <button @click="clearSearch" aria-label="Xoá tìm kiếm">✕</button>
          </span>
          <span v-if="params.category" class="filter-tag">
            {{ activeCategoryName }}
            <button @click="setCategory(null)" aria-label="Xoá danh mục">✕</button>
          </span>
          <span v-if="params.is_new" class="filter-tag">
            Mới nhất <button @click="toggleFilter('is_new', null)" aria-label="Xoá">✕</button>
          </span>
          <span v-if="params.is_featured" class="filter-tag">
            Nổi bật <button @click="toggleFilter('is_featured', null)" aria-label="Xoá">✕</button>
          </span>
        </div>

        <!-- Loading skeleton -->
        <div v-if="loading" class="products-grid">
          <div v-for="i in 12" :key="i" class="product-skeleton">
            <div class="skel-img" />
            <div class="skel-line w60" />
            <div class="skel-line w30" />
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="shop-error">
          <p>{{ error }}</p>
          <button class="reset-btn" @click="fetch">Thử lại</button>
        </div>

        <!-- Empty -->
        <div v-else-if="!products.length" class="shop-empty">
          <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1">
            <circle cx="32" cy="32" r="28"/>
            <path d="M20 32h24M32 20v24" opacity=".3"/>
          </svg>
          <p>Không tìm thấy sản phẩm phù hợp.</p>
          <button class="reset-btn" @click="resetFilters">Xoá bộ lọc</button>
        </div>

        <!-- Grid -->
        <div v-else class="products-grid">
          <ProductCard
            v-for="p in products"
            :key="p.id"
            :product="p"
            @quickAdd="handleQuickAdd"
          />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            class="page-btn"
            :disabled="params.page === 1"
            @click="goPage(params.page - 1)"
            aria-label="Trang trước"
          >←</button>

          <button
            v-for="p in pageNumbers"
            :key="p"
            class="page-btn"
            :class="{ active: p === params.page }"
            @click="goPage(p)"
          >{{ p }}</button>

          <button
            class="page-btn"
            :disabled="params.page === totalPages"
            @click="goPage(params.page + 1)"
            aria-label="Trang sau"
          >→</button>
        </div>
      </div>
    </div>

    <!-- Toast notification -->
    <Transition name="toast">
      <div v-if="toastMsg" class="toast" role="alert">
        <svg viewBox="0 0 20 20" fill="currentColor" class="toast-icon">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
        </svg>
        {{ toastMsg }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProductCard        from '@/components/ui/ProductCard.vue'
import { useProducts }    from '@/composables/useProducts'
import { categoriesApi }  from '@/api'
import { useCartStore }   from '@/stores/cart'

const route     = useRoute()
const router    = useRouter()
const cartStore = useCartStore()

// ── Filters ──────────────────────────────────────────────────────────────
const searchInput = ref('')
const sortBy      = ref('')
const sidebarOpen = ref(false)
const toastMsg    = ref('')
let   toastTimer  = null

// Init params from query string
const { products, total, loading, error, params, fetch } = useProducts({
  page:     Number(route.query.page)     || 1,
  per_page: 12,
  category: route.query.category         || undefined,
  search:   route.query.search           || undefined,
  is_new:   route.query.is_new === 'true' ? true : undefined,
})
searchInput.value = params.value.search ?? ''

// ── Categories from API ───────────────────────────────────────────────────
const categories = ref([])
categoriesApi.list().then(data => {
  // Only top-level non-root categories
  categories.value = data.filter(c => c.parent_id !== null)
})

// ── Computed ──────────────────────────────────────────────────────────────
const totalPages = computed(() => Math.ceil(total.value / params.value.per_page))

const pageNumbers = computed(() => {
  const pages = []
  const current = params.value.page
  const last    = totalPages.value
  for (let i = Math.max(1, current - 2); i <= Math.min(last, current + 2); i++) {
    pages.push(i)
  }
  return pages
})

const hasActiveFilters = computed(() =>
  !!(params.value.search || params.value.category || params.value.is_new || params.value.is_featured)
)

const activeCategoryName = computed(() => {
  const cat = categories.value.find(c => c.slug === params.value.category)
  return cat?.name ?? params.value.category
})

// ── Actions ───────────────────────────────────────────────────────────────
function setCategory(slug) {
  params.value = { ...params.value, category: slug ?? undefined, page: 1 }
  syncQuery()
}

function toggleFilter(key, val) {
  const cur = params.value[key]
  params.value = { ...params.value, [key]: cur === val ? undefined : val, page: 1 }
  syncQuery()
}

function applySearch() {
  params.value = { ...params.value, search: searchInput.value || undefined, page: 1 }
  syncQuery()
}

function clearSearch() {
  searchInput.value = ''
  params.value = { ...params.value, search: undefined, page: 1 }
  syncQuery()
}

function resetFilters() {
  searchInput.value = ''
  sortBy.value      = ''
  params.value = { page: 1, per_page: 12 }
  router.replace({ query: {} })
}

function goPage(p) {
  params.value = { ...params.value, page: p }
  syncQuery()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function applySort() {
  // Client-side sort (swap to server-side param when backend supports)
  if (sortBy.value === 'newest')     products.value.sort((a, b) => b.id - a.id)
  if (sortBy.value === 'price_asc')  products.value.sort((a, b) => a.price - b.price)
  if (sortBy.value === 'price_desc') products.value.sort((a, b) => b.price - a.price)
}

function syncQuery() {
  const q = {}
  if (params.value.page > 1)      q.page     = params.value.page
  if (params.value.category)      q.category = params.value.category
  if (params.value.search)        q.search   = params.value.search
  if (params.value.is_new)        q.is_new   = 'true'
  if (params.value.is_featured)   q.is_featured = 'true'
  router.replace({ query: q })
}

function handleQuickAdd(product) {
  const firstSize = product.sizes?.find(s => s.in_stock)?.size
  if (!firstSize) return
  cartStore.addItem(product, firstSize)
  clearTimeout(toastTimer)
  toastMsg.value = `Đã thêm "${product.name}" vào giỏ`
  toastTimer = setTimeout(() => { toastMsg.value = '' }, 2500)
}

// Close sidebar on route change / ESC
watch(() => route.fullPath, () => { sidebarOpen.value = false })
</script>

<style scoped>
/* ── Page hero ─────────────────────────────────────────── */
.shop-hero {
  background: var(--charcoal);
  padding: 64px 48px 56px;
  text-align: center;
}
.shop-hero .section-label { color: var(--gold); margin-bottom: 8px; }
.shop-title {
  font-family: var(--font-display);
  font-size: clamp(40px, 5vw, 72px);
  font-weight: 300;
  color: var(--cream);
  letter-spacing: 4px;
  margin-bottom: 12px;
}
.shop-sub {
  font-size: 12px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(245,240,232,.4);
}

/* ── Layout ────────────────────────────────────────────── */
.shop-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 80vh;
}

/* ── Sidebar ───────────────────────────────────────────── */
.shop-sidebar {
  background: var(--warm-white);
  border-right: 1px solid var(--border);
  padding: 40px 32px;
  position: sticky;
  top: 72px;
  height: calc(100vh - 72px);
  overflow-y: auto;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}
.sidebar-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 400;
}
.sidebar-close {
  display: none;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--text-muted);
}

.filter-group { margin-bottom: 32px; }
.filter-label {
  display: block;
  font-size: 9px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 14px;
}

.search-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border);
  padding: 10px 14px;
  transition: border-color var(--transition);
}
.search-wrap:focus-within { border-color: var(--charcoal); }
.search-icon { width: 16px; height: 16px; color: var(--text-muted); flex-shrink: 0; }
.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-body);
  font-size: 12px;
  outline: none;
  color: var(--charcoal);
}
.search-input::placeholder { color: var(--border); }

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.filter-chip {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  border: 1px solid var(--border);
  padding: 6px 14px;
  background: transparent;
  font-family: var(--font-body);
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition);
}
.filter-chip:hover  { border-color: var(--charcoal); color: var(--charcoal); }
.filter-chip.active { border-color: var(--charcoal); background: var(--charcoal); color: var(--cream); }

.reset-btn {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  background: none;
  border: 1px solid var(--border);
  padding: 10px 20px;
  font-family: var(--font-body);
  color: var(--text-muted);
  cursor: pointer;
  width: 100%;
  transition: all var(--transition);
}
.reset-btn:hover { border-color: var(--charcoal); color: var(--charcoal); }

/* ── Main area ─────────────────────────────────────────── */
.shop-main {
  padding: 40px 48px;
  background: var(--warm-white);
}

/* Toolbar */
.shop-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}
.filter-toggle-btn {
  display: none;
  align-items: center;
  gap: 8px;
  background: none;
  border: 1px solid var(--border);
  padding: 8px 16px;
  font-family: var(--font-body);
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  cursor: pointer;
  color: var(--charcoal);
  transition: all var(--transition);
}
.filter-toggle-btn svg { width: 16px; height: 16px; }
.filter-toggle-btn:hover { border-color: var(--charcoal); }
.toolbar-count {
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 1px;
  flex: 1;
}
.sort-select {
  font-family: var(--font-body);
  font-size: 11px;
  letter-spacing: 1px;
  border: 1px solid var(--border);
  padding: 8px 14px;
  background: transparent;
  color: var(--charcoal);
  outline: none;
  cursor: pointer;
}

/* Active filter tags */
.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}
.filter-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  background: var(--charcoal);
  color: var(--cream);
  padding: 4px 12px;
}
.filter-tag button {
  background: none;
  border: none;
  color: rgba(245,240,232,.6);
  cursor: pointer;
  font-size: 12px;
  line-height: 1;
  transition: color var(--transition);
}
.filter-tag button:hover { color: var(--cream); }

/* Products grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px 24px;
  margin-bottom: 48px;
}

/* Skeleton */
.product-skeleton { cursor: default; }
.skel-img {
  aspect-ratio: 3/4;
  background: var(--cream-dark);
  margin-bottom: 14px;
  animation: shimmer 1.5s ease infinite;
}
.skel-line {
  height: 12px;
  background: var(--cream-dark);
  margin-bottom: 8px;
  border-radius: 2px;
  animation: shimmer 1.5s ease infinite;
}
.skel-line.w60 { width: 60%; }
.skel-line.w30 { width: 30%; }
@keyframes shimmer {
  0%,100% { opacity: 1; } 50% { opacity: .45; }
}

/* Empty / Error */
.shop-empty, .shop-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  min-height: 40vh;
  color: var(--text-muted);
  text-align: center;
}
.shop-empty svg { width: 64px; height: 64px; opacity: .3; }
.shop-empty p, .shop-error p { font-size: 14px; letter-spacing: .5px; }
.shop-empty .reset-btn, .shop-error .reset-btn { width: auto; }

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  padding-top: 40px;
  border-top: 1px solid var(--border);
}
.page-btn {
  width: 40px; height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  font-family: var(--font-body);
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition);
  display: flex; align-items: center; justify-content: center;
}
.page-btn:hover:not(:disabled) { border-color: var(--charcoal); color: var(--charcoal); }
.page-btn.active { background: var(--charcoal); border-color: var(--charcoal); color: var(--cream); }
.page-btn:disabled { opacity: .3; cursor: default; }

/* Toast */
.toast {
  position: fixed;
  bottom: 32px; left: 50%;
  transform: translateX(-50%);
  background: var(--charcoal);
  color: var(--cream);
  display: flex; align-items: center; gap: 10px;
  padding: 14px 28px;
  font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
  z-index: 2000;
  box-shadow: 0 8px 32px rgba(0,0,0,.2);
  white-space: nowrap;
}
.toast-icon { width: 16px; height: 16px; color: var(--gold); flex-shrink: 0; }
.toast-enter-active, .toast-leave-active { transition: opacity .3s ease, transform .3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(12px); }
</style>
