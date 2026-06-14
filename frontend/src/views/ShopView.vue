<template>
  <div class="shop-page">

    <h1 class="page-title">TẤT CẢ SẢN PHẨM</h1>

    <div class="shop-layout">

      <!-- ── Sidebar ── -->
      <aside class="shop-sidebar">

        <div class="filter-section">
          <h3 class="filter-title">BỘ LỌC</h3>

          <div class="category-list">
            <!-- Tất cả -->
            <label class="cat-item">
              <input type="checkbox" :checked="!selectedCategory" @change="setCategory(null)" />
              <span>Tất cả</span>
            </label>

            <!-- Áo Dài -->
            <label class="cat-item">
              <input type="checkbox" :checked="selectedCategory === 'ao-dai'" @change="setCategory('ao-dai')" />
              <span>Áo Dài</span>
            </label>

            <!-- Pháp Phục -->
            <label class="cat-item">
              <input type="checkbox" :checked="selectedCategory === 'phap-phuc'" @change="setCategory('phap-phuc')" />
              <span>Pháp Phục</span>
            </label>

            <!-- Đầm Lụa -->
            <label class="cat-item">
              <input type="checkbox" :checked="selectedCategory === 'dam-lua'" @change="setCategory('dam-lua')" />
              <span>Đầm Lụa</span>
            </label>

            <!-- Khăn Lụa + 3 sub -->
            <label class="cat-item">
              <input type="checkbox" :checked="selectedCategory === 'khan-lua'" @change="setCategory('khan-lua')" />
              <span>Khăn Lụa</span>
            </label>
            <label class="cat-item cat-sub">
              <input type="checkbox" :checked="selectedCategory === 'khan-lua-ve-tay-cao-cap'" @change="setCategory('khan-lua-ve-tay-cao-cap')" />
              <span>Khăn lụa vẽ tay cao cấp</span>
            </label>
            <label class="cat-item cat-sub">
              <input type="checkbox" :checked="selectedCategory === 'khan-lua-loang-tia-cao-cap'" @change="setCategory('khan-lua-loang-tia-cao-cap')" />
              <span>Khăn lụa loang tia cao cấp</span>
            </label>
            <label class="cat-item cat-sub">
              <input type="checkbox" :checked="selectedCategory === 'khan-lua-tron-cao-cap'" @change="setCategory('khan-lua-tron-cao-cap')" />
              <span>Khăn lụa trơn cao cấp</span>
            </label>

            <!-- Lụa Tơ Tằm — chỉ là link, không checkbox -->
            <RouterLink to="/lua-to-tam" class="lua-link">Chọn mẫu Lụa Tơ Tằm</RouterLink>
          </div>
        </div>

        <button class="btn-filter" @click="applyFilter">TÌM THEO BỘ LỌC</button>
        <button class="btn-reset" @click="resetFilters">BỎ BỘ LỌC</button>

      </aside>

      <!-- ── Main ── -->
      <main class="shop-main">

        <!-- Loading -->
        <div v-if="loading" class="product-grid">
          <div v-for="i in 12" :key="i" class="skeleton">
            <div class="skel-img" />
            <div class="skel-line" style="width:60%" />
            <div class="skel-line" style="width:40%" />
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="feedback">
          <p>{{ error }}</p>
          <button class="btn-reset" @click="fetch">Thử lại</button>
        </div>

        <!-- Empty -->
        <div v-else-if="!products.length" class="feedback">
          <p>Không tìm thấy sản phẩm phù hợp.</p>
          <button class="btn-reset" @click="resetFilters">Bỏ bộ lọc</button>
        </div>

        <!-- Grid -->
        <div v-else class="product-grid">
          <RouterLink
            v-for="p in products"
            :key="p.id"
            :to="`/san-pham/${p.slug}`"
            class="product-card"
          >
            <div class="product-img-wrap">
              <img
                v-if="p.images && p.images.length"
                :src="p.images[0].url"
                :alt="p.name"
                class="product-img"
              />
              <div v-else class="product-img-placeholder" :style="{ background: placeholderBg(p) }" />
              <span v-if="p.is_new" class="badge-new">Mới</span>
            </div>
            <p class="product-name">{{ p.name }}</p>
            <p class="product-price">{{ formatPrice(p.price) }}</p>
          </RouterLink>
        </div>

        <!-- Phân trang -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="pg-btn" :disabled="params.page === 1" @click="goPage(params.page - 1)">←</button>
          <button
            v-for="n in pageNumbers" :key="n"
            class="pg-btn" :class="{ active: n === params.page }"
            @click="goPage(n)"
          >{{ n }}</button>
          <button class="pg-btn" :disabled="params.page === totalPages" @click="goPage(params.page + 1)">→</button>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProducts }   from '@/composables/useProducts'

const route  = useRoute()
const router = useRouter()

// Filter state — khởi tạo từ URL query
const selectedCategory = ref(route.query.category || null)

const { products, total, loading, error, params, fetch } = useProducts({
  page:     Number(route.query.page) || 1,
  per_page: 12,
  category: selectedCategory.value || undefined,
})

// Khi menu header navigate vào /cua-hang?category=xxx thì tự apply
watch(() => route.query.category, (newCat) => {
  selectedCategory.value = newCat || null
  params.value = { ...params.value, category: newCat || undefined, page: 1 }
})

// ── Computed ──────────────────────────────────────────────────────────────
const totalPages = computed(() => Math.ceil(total.value / params.value.per_page))
const pageNumbers = computed(() => {
  const pages = [], cur = params.value.page, last = totalPages.value
  for (let i = Math.max(1, cur - 2); i <= Math.min(last, cur + 2); i++) pages.push(i)
  return pages
})

// ── Actions ───────────────────────────────────────────────────────────────
function setCategory(slug) {
  selectedCategory.value = slug
}

function applyFilter() {
  params.value = { ...params.value, category: selectedCategory.value || undefined, page: 1 }
  const q = {}
  if (selectedCategory.value) q.category = selectedCategory.value
  router.replace({ query: q })
}

function resetFilters() {
  selectedCategory.value = null
  params.value = { page: 1, per_page: 12 }
  router.replace({ query: {} })
}

function goPage(p) {
  params.value = { ...params.value, page: p }
  const q = {}
  if (params.value.category) q.category = params.value.category
  if (p > 1) q.page = p
  router.replace({ query: q })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── Helpers ───────────────────────────────────────────────────────────────
const COLORS = ['#D4B896','#A8C4BC','#C4A8B8','#B8C4A8','#C4B4A0','#A0B8C4']
function placeholderBg(p) {
  return COLORS[p.id % COLORS.length]
}

function formatPrice(price) {
  if (!price) return ''
  const num = Number(price)
  return num.toLocaleString('vi-VN') + ' đ'
}
</script>

<style scoped>
/* ── Tổng thể ── */
.shop-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: 32px 48px 64px;
}

/* ── Tiêu đề ── */
.page-title {
  font-family: var(--font-display);
  font-size: 40px;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--brand-red);
  text-align: center;
  margin-bottom: 32px;
}

/* ── Layout ── */
.shop-layout {
  display: flex;
  gap: 28px;
  max-width: 1300px;
  margin: 0 auto;
  align-items: flex-start;
}

/* ── Sidebar ── */
.shop-sidebar {
  width: 300px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.filter-section { margin-bottom: 24px; }

.filter-title {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin-bottom: 16px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 4px;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  transition: color var(--transition);
}
.cat-item:hover { color: var(--brand-red); }

.cat-item input[type="checkbox"] {
  accent-color: var(--brand-red);
  width: 15px;
  height: 15px;
  flex-shrink: 0;
  cursor: pointer;
}

/* Sub-categories indent */
.cat-sub {
  padding-left: 24px;
}

/* Lụa Tơ Tằm link */
.lua-link {
  display: inline-block;
  margin-top: 8px;
  padding: 6px 4px;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--brand-red);
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
  transition: opacity var(--transition);
}
.lua-link:hover { opacity: 0.7; }

/* Buttons */
.btn-filter {
  width: 100%;
  padding: 13px;
  background: var(--brand-red);
  border: none;
  border-radius: 999px;
  color: #fff;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background var(--transition);
}
.btn-filter:hover { background: var(--brand-dark); }

.btn-reset {
  width: 100%;
  padding: 12px;
  background: #fff;
  border: 1.5px solid var(--brand-red);
  border-radius: 999px;
  color: var(--brand-red);
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}
.btn-reset:hover { background: var(--brand-red); color: #fff; }

/* ── Main ── */
.shop-main {
  flex: 1;
  min-width: 0;
}

/* ── Product grid 4 cột ── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  display: block;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

/* Ảnh dài hơn: aspect-ratio 3/5 */
.product-img-wrap {
  width: 100%;
  aspect-ratio: 3 / 5;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
  position: relative;
  background: #e8e4dc;
  transition: transform var(--transition), box-shadow var(--transition);
}
.product-card:hover .product-img-wrap {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,.12);
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.product-img-placeholder {
  width: 100%;
  height: 100%;
}

.badge-new {
  position: absolute;
  top: 10px; left: 10px;
  background: var(--brand-red);
  color: #fff;
  font-family: var(--font-body);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 4px 9px;
  border-radius: 2px;
}

.product-name {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: var(--text-dark);
  text-align: center;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.product-price {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-medium);
  text-align: center;
}

/* ── Skeleton ── */
.skel-img {
  aspect-ratio: 3 / 5;
  background: #e0ddd8;
  border-radius: 10px;
  margin-bottom: 10px;
  animation: pulse 1.5s ease infinite;
}
.skel-line {
  height: 11px;
  background: #e0ddd8;
  margin: 0 auto 7px;
  border-radius: 3px;
  animation: pulse 1.5s ease infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.45} }

/* ── Feedback ── */
.feedback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  min-height: 40vh;
  color: var(--text-medium);
  font-size: 14px;
  text-align: center;
}
.feedback .btn-reset { width: auto; padding: 12px 32px; }

/* ── Pagination ── */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid #ddd;
}
.pg-btn {
  width: 38px; height: 38px;
  border: 1px solid #ddd;
  background: transparent;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-medium);
  cursor: pointer;
  border-radius: 4px;
  display: flex; align-items: center; justify-content: center;
  transition: all .2s;
}
.pg-btn:hover:not(:disabled) { border-color: var(--brand-red); color: var(--brand-red); }
.pg-btn.active { background: var(--brand-red); border-color: var(--brand-red); color: #fff; }
.pg-btn:disabled { opacity: .3; cursor: default; }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .product-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .shop-page { padding: 24px 20px 48px; }
  .shop-layout { flex-direction: column; }
  .shop-sidebar { width: 100%; }
  .product-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
