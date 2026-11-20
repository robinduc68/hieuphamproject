<template>
  <div class="fabric-page">

    <!-- ── Page header ─────────────────────────────────── -->
    <header class="fabric-header">
      <h1 class="fabric-header-title">
        Lụa Nha Xá 100% tơ tằm
        <span class="fabric-header-sub">(Được dệt hoàn toàn bằng sợi tơ tằm)</span>
      </h1>
    </header>

    <button class="filter-toggle" :aria-expanded="filtersOpen" @click="filtersOpen = !filtersOpen">
      BỘ LỌC
      <span v-if="selectedTypes.length + selectedColors.length" class="filter-toggle-count">{{ selectedTypes.length + selectedColors.length }}</span>
      <svg class="filter-toggle-caret" :class="{ open: filtersOpen }" viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 1l5 5 5-5"/></svg>
    </button>

    <div class="fabric-layout">

      <!-- ── Sidebar ─────────────────────────────────────── -->
      <aside class="fabric-sidebar" :class="{ 'is-open': filtersOpen }">

        <!-- LOẠI LỤA -->
        <div class="filter-section">
          <div class="pattern-list">
            <label
              v-for="t in silkTypes"
              :key="t"
              class="pattern-item"
            >
              <input type="checkbox" v-model="selectedTypes" :value="t" />
              <span>{{ t }}</span>
            </label>
          </div>
        </div>

        <!-- MÀU SẮC -->
        <div class="filter-section">
          <h3 class="filter-title">MÀU SẮC</h3>
          <div class="color-grid">
            <div
              v-for="c in colors"
              :key="c.name"
              class="color-item"
              :class="{ selected: selectedColors.includes(c.name) }"
              @click="toggleColor(c.name)"
            >
              <div
                class="color-swatch"
                :style="{ background: c.hex, border: c.hex === '#FFFFFF' ? '1px solid #ddd' : 'none' }"
              />
              <span class="color-name">{{ c.name }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <button class="btn-filter" @click="applyFilter">TÌM THEO BỘ LỌC</button>
        <button class="btn-reset" @click="resetFilter">BỎ BỘ LỌC</button>

      </aside>

      <!-- ── Main grid ───────────────────────────────────── -->
      <main class="fabric-main">
        <p class="fabric-desc">Chọn mẫu vải để thiết kế bộ áo dài, pháp phục của riêng bạn.</p>

        <div class="fabric-grid" :aria-busy="loading">
          <!-- Khung chờ trong lúc tải sản phẩm -->
          <template v-if="loading">
            <div v-for="n in 12" :key="`sk-${n}`" class="fabric-card fabric-skeleton" aria-hidden="true">
              <div class="fabric-img skeleton-box" />
              <div class="skeleton-line" />
            </div>
          </template>

          <!-- Vải thật tạo từ trang admin (bộ lọc loại lụa/màu chỉ áp dụng cho mẫu demo) -->
          <RouterLink
            v-for="p in pagedProducts"
            :key="`p-${p.id}`"
            :to="`/san-pham/${p.slug}`"
            class="fabric-card"
          >
            <div class="fabric-img" :style="{ background: productGradient(p) }">
              <img v-if="productImage(p)" :src="productImage(p)" :alt="p.name" class="fabric-photo" />
              <div v-else class="fabric-shimmer" />
            </div>
            <p class="fabric-name">{{ p.name }}</p>
          </RouterLink>

          <RouterLink
            v-for="fabric in displayedFabrics"
            :key="fabric.id"
            :to="`/lua-nha-xa-100-to-tam/${fabric.id}`"
            class="fabric-card"
          >
            <div class="fabric-img" :style="{ background: fabricGradient(fabric.color1, fabric.color2) }">
              <div class="fabric-shimmer" />
            </div>
            <p class="fabric-name">{{ fabric.name }}</p>
          </RouterLink>
        </div>

        <!-- Phân trang -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="pg-btn" :disabled="currentPage === 1" @click="goPage(currentPage - 1)">←</button>
          <button
            v-for="n in pageNumbers" :key="n"
            class="pg-btn" :class="{ active: n === currentPage }"
            @click="goPage(n)"
          >{{ n }}</button>
          <button class="pg-btn" :disabled="currentPage === totalPages" @click="goPage(currentPage + 1)">→</button>
        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { pureSilkFabrics, silkTypes, colors, fabricGradient } from '@/data/fabrics'
import { useFabricProducts, productImage, productGradient } from '@/composables/useFabricProducts'

const { pureSilk: fabricProducts, loading } = useFabricProducts()

const selectedTypes  = ref([])
const selectedColors = ref([])
const filtersOpen    = ref(false)   // bộ lọc trên mobile

// Sản phẩm thật: lọc theo loại lụa/tone màu admin đã gán. Chưa gán → ẩn khi
// khách bật bộ lọc tương ứng (không đoán bừa là khớp).
const shownProducts = computed(() => {
  let list = fabricProducts.value
  if (selectedTypes.value.length)
    list = list.filter(p => selectedTypes.value.includes((p.silk_type || '').trim()))
  if (selectedColors.value.length)
    list = list.filter(p => selectedColors.value.includes((p.color_tag || '').trim()))
  return list
})

const displayedFabrics = computed(() => {
  let list = pureSilkFabrics
  if (selectedTypes.value.length)
    list = list.filter(f => selectedTypes.value.includes(f.silkType))
  if (selectedColors.value.length)
    list = list.filter(f => selectedColors.value.includes(f.colorTag))
  return list
})

// ── Phân trang (số trang nằm trên URL ?page= để bấm Back quay lại đúng trang) ──
const PER_PAGE = 24
const route  = useRoute()
const router = useRouter()

const totalPages = computed(() => Math.max(1, Math.ceil(shownProducts.value.length / PER_PAGE)))
// ?page= vượt quá số trang hiện có → hiện trang cuối
const currentPage = computed(() =>
  Math.min(Math.max(1, Number(route.query.page) || 1), totalPages.value)
)
const pagedProducts = computed(() =>
  shownProducts.value.slice((currentPage.value - 1) * PER_PAGE, currentPage.value * PER_PAGE)
)
const pageNumbers = computed(() => {
  const pages = [], cur = currentPage.value, last = totalPages.value
  for (let i = Math.max(1, cur - 2); i <= Math.min(last, cur + 2); i++) pages.push(i)
  return pages
})

function pageQuery(p) {
  const { page, ...rest } = route.query
  return p > 1 ? { ...rest, page: p } : rest
}

function goPage(p) {
  router.push({ query: pageQuery(p) })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Đổi bộ lọc → về trang 1
watch([selectedTypes, selectedColors], () => {
  if (route.query.page) router.replace({ query: pageQuery(1) })
}, { deep: true })

function toggleColor(name) {
  const i = selectedColors.value.indexOf(name)
  if (i === -1) selectedColors.value.push(name)
  else selectedColors.value.splice(i, 1)
}

function applyFilter() { /* filter is already reactive */ }

function resetFilter() {
  selectedTypes.value  = []
  selectedColors.value = []
}

</script>

<style scoped>
.fabric-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: var(--page-top) var(--page-x) 64px;
}

.fabric-header {
  max-width: 1300px;
  margin: 0 auto 22px;
  text-align: left;
}

.fabric-header-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--brand-red);
}

.fabric-header-sub {
  font-size: 16px;
  font-weight: 400;
  font-style: italic;
  letter-spacing: 0;
  color: inherit;
}

.fabric-layout {
  display: flex;
  gap: 28px;
  max-width: 1300px;
  margin: 0 auto;
  align-items: flex-start;
}

/* ── Sidebar ─────────────────────────────────────────── */
.fabric-sidebar {
  width: 300px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.filter-section {
  margin-bottom: 24px;
}

.filter-title {
  font-family: var(--font-body);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin-bottom: 14px;
}

.filter-search {
  width: 100%;
  padding: 11px 16px;
  border: 1px solid #ddd;
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--text-dark);
  outline: none;
  margin-bottom: 12px;
  transition: border-color var(--transition);
}
.filter-search:focus { border-color: var(--brand-red); }
.filter-search::placeholder { color: #bbb; }

/* Chiều cao 1 dòng: 7px + 18px + 7px — dùng để chốt khung 8 dòng */
.pattern-list {
  --pattern-row: 36px;
  --pattern-gap: 2px;
  display: flex;
  flex-direction: column;
  gap: var(--pattern-gap);
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-width: thin;
  scrollbar-color: #d6d6d6 transparent;
  padding-right: 6px;
}
.pattern-list::-webkit-scrollbar { width: 6px; }
.pattern-list::-webkit-scrollbar-track { background: transparent; }
.pattern-list::-webkit-scrollbar-thumb {
  background: #d6d6d6;
  border-radius: 3px;
}
.pattern-list::-webkit-scrollbar-thumb:hover { background: var(--brand-red); }

.pattern-empty {
  padding: 8px 4px;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--text-muted);
  font-style: italic;
}

.pattern-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 4px;
  line-height: 20px;
  flex-shrink: 0;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--text-dark);
  transition: color var(--transition);
}
.pattern-item:hover { color: var(--brand-red); }
.pattern-item input[type="checkbox"] {
  accent-color: var(--brand-red);
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* Color grid */
.color-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px 8px;
}
.color-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}
.color-swatch {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  transition: transform var(--transition), box-shadow var(--transition);
}
.color-item:hover .color-swatch,
.color-item.selected .color-swatch {
  transform: scale(1.1);
  box-shadow: 0 0 0 2px var(--brand-red);
}
.color-name {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  text-align: center;
}

/* Buttons */
.btn-filter {
  width: 100%;
  padding: 15px;
  background: var(--brand-red);
  border: none;
  border-radius: 999px;
  color: #fff;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background var(--transition);
}
.btn-filter:hover { background: var(--brand-dark); }

.btn-reset {
  width: 100%;
  padding: 14px;
  background: #fff;
  border: 1.5px solid var(--brand-red);
  border-radius: 999px;
  color: var(--brand-red);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}
.btn-reset:hover { background: var(--brand-red); color: #fff; }

/* ── Main ────────────────────────────────────────────── */
.fabric-main {
  flex: 1;
  min-width: 0;
}

.fabric-desc {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--text-dark);
  margin-bottom: 24px;
}

.fabric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.fabric-card {
  cursor: pointer;
  display: block;
  color: inherit;
  text-decoration: none;
}

.fabric-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  margin-bottom: 10px;
  transition: transform var(--transition), box-shadow var(--transition);
}
.fabric-card:hover .fabric-img {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,.15);
}

.fabric-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.fabric-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0)    0%,
    rgba(255,255,255,.18) 45%,
    rgba(255,255,255,.32) 50%,
    rgba(255,255,255,.18) 55%,
    rgba(255,255,255,0)   100%
  );
  pointer-events: none;
}

.fabric-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: var(--text-dark);
  text-align: center;
  text-transform: uppercase;
}

/* ── Khung chờ khi đang tải ── */
.fabric-skeleton { cursor: default; pointer-events: none; }
.skeleton-box,
.skeleton-line {
  background: linear-gradient(90deg, #e9e3d8 25%, #f4f0e8 50%, #e9e3d8 75%);
  background-size: 200% 100%;
  animation: skeleton-shine 1.4s ease-in-out infinite;
}
.skeleton-line {
  width: 70%;
  height: 14px;
  margin: 0 auto;
  border-radius: 4px;
}
@keyframes skeleton-shine {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton-box, .skeleton-line { animation: none; }
}

/* ── Phân trang (cùng kiểu với trang Cửa hàng) ── */
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

/* Bộ lọc trên mobile: gập lại sau nút, tránh đẩy lưới sản phẩm xuống quá xa */
.filter-toggle {
  display: none;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  margin-bottom: 14px;
  padding: 13px 16px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  color: var(--charcoal);
}
.filter-toggle-count {
  margin-left: auto;
  padding: 1px 8px;
  border-radius: 999px;
  background: var(--brand-red);
  color: #fff;
  font-size: 11px;
  letter-spacing: 0;
}
.filter-toggle-caret { width: 12px; height: 8px; transition: transform var(--transition); flex-shrink: 0; }
.filter-toggle-caret.open { transform: rotate(180deg); }

@media (max-width: 1024px) {
  .fabric-grid { grid-template-columns: repeat(3, 1fr); }
  .color-grid  { grid-template-columns: repeat(6, 1fr); }
}
@media (max-width: 900px) {
  .fabric-layout  { flex-direction: column; }
  .fabric-sidebar { width: 100%; display: none; }
  .fabric-sidebar.is-open { display: flex; }
  .filter-toggle  { display: flex; }
  .fabric-header-title { font-size: 26px; }
  .fabric-header-sub   { display: block; font-size: 14px; margin-top: 4px; }
}
@media (max-width: 560px) {
  .fabric-page { padding-bottom: 48px; }
  .fabric-grid { grid-template-columns: repeat(2, 1fr); gap: 14px; }
  .color-grid  { grid-template-columns: repeat(4, 1fr); }
  .fabric-name { font-size: 13px; }
}
</style>
