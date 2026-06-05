<template>
  <div class="product-detail-page">

    <!-- Loading skeleton -->
    <div v-if="loading" class="pd-skeleton">
      <div class="skeleton-gallery">
        <div class="skeleton-thumb-col">
          <div v-for="i in 4" :key="i" class="skeleton-thumb" />
        </div>
        <div class="skeleton-main-img" />
      </div>
      <div class="skeleton-info">
        <div class="skeleton-line w-40" />
        <div class="skeleton-line w-70 tall" />
        <div class="skeleton-line w-30" />
        <div class="skeleton-line w-full" />
        <div class="skeleton-line w-full" />
        <div class="skeleton-line w-60" />
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="pd-error">
      <p>{{ error }}</p>
      <RouterLink to="/" class="back-link">← Về trang chủ</RouterLink>
    </div>

    <!-- Product loaded -->
    <template v-else-if="product">
      <div class="pd-wrapper">

        <!-- Breadcrumb -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <RouterLink to="/">Home Page</RouterLink>
          <span class="sep">/</span>
          <RouterLink v-if="product.category" :to="`/danh-muc/${product.category.slug}`">
            {{ product.category.name }}
          </RouterLink>
          <span class="sep">/</span>
          <RouterLink v-if="product.sub_category" :to="`/danh-muc/${product.category?.slug}`">
            {{ product.sub_category }}
          </RouterLink>
          <span class="sep">/</span>
          <span class="breadcrumb-current" aria-current="page">{{ product.name }}</span>
        </nav>

        <div class="pd-layout">
        <!-- ── Gallery ─────────────────────────────────────────────── -->
        <div class="pd-gallery">
          <!-- Thumbnail strip -->
          <div class="thumb-strip">
            <button
              v-for="(img, i) in displayImages"
              :key="i"
              class="thumb-btn"
              :class="{ active: activeImg === i }"
              :aria-label="`Xem ảnh ${i + 1}`"
              @click="activeImg = i"
            >
              <div
                class="thumb-swatch"
                :style="{ background: swatchGradient(img.color_hex) }"
              />
            </button>
          </div>

          <!-- Main image -->
          <div class="main-img-wrap">
            <div
              class="main-img"
              :style="{ background: swatchGradient(displayImages[activeImg]?.color_hex) }"
            >
              <!-- Overlay text (matches real site) -->
              <div class="img-overlay-text" aria-hidden="true">
                <span class="overlay-category">
                  {{ product.sub_category || product.category?.name || 'HUY VO' }}
                </span>
                <span class="overlay-logo">HU<em>Y</em>VO</span>
              </div>

              <!-- Badge -->
              <span v-if="product.is_new" class="img-badge">New</span>
            </div>
          </div>
        </div>

        <!-- ── Info panel ──────────────────────────────────────────── -->
        <div class="pd-info">

          <!-- Tên & giá -->
          <h1 class="pd-name">{{ product.name.toUpperCase() }}</h1>
          <p class="pd-price">{{ displayPrice }}</p>

          <!-- ── Lựa chọn hình thức may ── -->
          <div class="pd-option">
            <p class="opt-label">Lựa chọn hình thức may</p>
            <div class="opt-method-row">
              <div class="opt-method-left">
                <span class="opt-sublabel">May theo size</span>
                <div class="sizes-grid">
                  <button
                    v-for="sz in product.sizes"
                    :key="sz.id"
                    class="size-btn"
                    :class="{ active: selectedSize === sz.size && tailoringMethod === 'size', disabled: !sz.in_stock }"
                    :disabled="!sz.in_stock"
                    @click="selectSize(sz.size)"
                  >{{ sz.size }}</button>
                </div>
              </div>
              <button
                class="method-alt-btn"
                :class="{ active: tailoringMethod === 'custom' }"
                @click="tailoringMethod = 'custom'; selectedSize = null; sizeError = false"
              >May theo số đo</button>
            </div>
            <div class="opt-links">
              <button class="opt-link" @click="sizeGuideOpen = true">Hướng dẫn chọn size</button>
              <button class="opt-link">Hướng dẫn lấy số đo &amp; đặt may</button>
            </div>
            <p v-if="sizeError" class="opt-error" role="alert">Vui lòng chọn size hoặc chọn may theo số đo</p>
          </div>

          <!-- ── Lựa chọn tà trong ── -->
          <div class="pd-option">
            <p class="opt-label">Lựa chọn tà trong</p>
            <div class="opt-choice-row">
              <button class="choice-btn" :class="{ active: liningType === 'yem_roi' }" @click="liningType = 'yem_roi'">May yếm rời</button>
              <button class="choice-btn" :class="{ active: liningType === 'lien_ta' }" @click="liningType = 'lien_ta'">May liền tà ngoài</button>
            </div>
          </div>

          <!-- ── Lựa chọn màu sắc ── -->
          <div class="pd-option">
            <p class="opt-label">Lựa chọn màu sắc</p>
            <div class="opt-choice-row">
              <button class="choice-btn" :class="{ active: colorOption === 'same' }" @click="colorOption = 'same'">Giống ảnh mẫu</button>
              <button class="choice-btn" :class="{ active: colorOption === 'custom_color' }" @click="colorOption = 'custom_color'">Phối màu riêng</button>
            </div>
            <div class="opt-links opt-links--end">
              <button class="opt-link">Hướng dẫn chọn màu &amp; đặt may</button>
            </div>
          </div>

          <!-- ── Ghi chú ── -->
          <div class="pd-note-wrap">
            <input
              v-model="note"
              type="text"
              class="pd-note-input"
              placeholder="Ghi chú (nếu cần): Dáng suông (có chiết eo),..."
            />
          </div>

          <!-- ── Thêm vào giỏ ── -->
          <button
            class="add-to-cart-btn"
            :class="{ added: justAdded }"
            @click="handleAddToCart"
          >
            <span v-if="!justAdded">THÊM VÀO GIỎ HÀNG</span>
            <span v-else class="added-label">
              <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              ĐÃ THÊM VÀO GIỎ
            </span>
          </button>

          <!-- ── Accordion ── -->
          <div class="pd-accordion">
            <div v-for="tab in tabs" :key="tab.key" class="accordion-item">
              <button
                class="accordion-trigger"
                :aria-expanded="openTab === tab.key"
                @click="openTab = openTab === tab.key ? null : tab.key"
              >
                {{ tab.label }}
                <svg class="accordion-icon" :class="{ rotated: openTab === tab.key }"
                  viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M1 1l5 5 5-5"/>
                </svg>
              </button>
              <Transition name="accordion">
                <div v-if="openTab === tab.key" class="accordion-body">
                  <p>{{ tab.content }}</p>
                </div>
              </Transition>
            </div>
          </div>

        </div>
        </div><!-- end pd-layout -->
      </div><!-- end pd-wrapper -->

      <!-- Related products carousel -->
      <section v-if="related.length" class="pd-related">
        <div class="pd-related-inner">

          <h2 class="related-title">SẢN PHẨM LIÊN QUAN</h2>

          <div class="rel-carousel">
            <!-- Prev arrow -->
            <button class="rel-arrow rel-arrow--prev" @click="relatedPrev" :disabled="relatedAtStart" aria-label="Trước">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M15 19l-7-7 7-7"/></svg>
            </button>

            <!-- Viewport -->
            <div class="rel-viewport" ref="relatedVp">
              <div class="rel-track" :style="relatedTrackStyle">
                <RouterLink
                  v-for="p in related"
                  :key="p.id"
                  :to="`/san-pham/${p.slug}`"
                  class="rel-slide"
                  :style="relatedItemW ? { width: relatedItemW + 'px' } : {}"
                >
                  <div class="rel-img">
                    <div class="rel-swatch" :style="{ background: swatchGradient(p.images?.[0]?.color_hex ?? p.color) }">
                      <div class="rel-img-overlay" aria-hidden="true">
                        <span class="rel-overlay-sub">{{ p.sub_category || 'ÁO DÀI' }}</span>
                        <span class="rel-overlay-logo">HU<em>Y</em>VO</span>
                      </div>
                    </div>
                  </div>
                  <div class="rel-info">
                    <h3 class="rel-name">{{ p.name.toUpperCase() }}</h3>
                    <p class="rel-price">{{ typeof p.price === 'number' ? formatPrice(p.price) : p.price }}</p>
                  </div>
                </RouterLink>
              </div>
            </div>

            <!-- Next arrow -->
            <button class="rel-arrow rel-arrow--next" @click="relatedNext" :disabled="relatedAtEnd" aria-label="Tiếp theo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>

        </div>
      </section>
    </template>

    <!-- Size Guide Modal -->
    <Teleport to="body">
      <Transition name="overlay">
        <div v-if="sizeGuideOpen" class="modal-overlay" @click="sizeGuideOpen = false" />
      </Transition>
      <Transition name="modal">
        <div v-if="sizeGuideOpen" class="modal" role="dialog" aria-modal="true" aria-label="Size guide">
          <div class="modal-header">
            <h3 class="modal-title">Hướng Dẫn Chọn Size</h3>
            <button class="modal-close" @click="sizeGuideOpen = false" aria-label="Đóng">✕</button>
          </div>
          <div class="modal-body">
            <table class="size-table">
              <thead>
                <tr><th>Size</th><th>Ngực (cm)</th><th>Eo (cm)</th><th>Hông (cm)</th><th>Chiều cao (cm)</th></tr>
              </thead>
              <tbody>
                <tr v-for="row in sizeGuideRows" :key="row.size">
                  <td>{{ row.size }}</td>
                  <td>{{ row.chest }}</td>
                  <td>{{ row.waist }}</td>
                  <td>{{ row.hip }}</td>
                  <td>{{ row.height }}</td>
                </tr>
              </tbody>
            </table>
            <p class="size-note">* Số đo tính theo cm. Nếu số đo nằm giữa 2 size, chọn size lớn hơn.</p>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute }             from 'vue-router'
import { useProduct }           from '@/composables/useProducts'
import { useNewArrivals }       from '@/composables/useProducts'
import { useCartStore }         from '@/stores/cart'
import ProductCard              from '@/components/ui/ProductCard.vue'

const route      = useRoute()
const cartStore  = useCartStore()
const slug       = computed(() => route.params.slug)

const { product, loading, error } = useProduct(slug)
const { products: allProducts }   = useNewArrivals(8)

// Local UI state
const activeImg        = ref(0)
const selectedSize     = ref(null)
const sizeError        = ref(false)
const openTab          = ref(null)
const justAdded        = ref(false)
const sizeGuideOpen    = ref(false)
const customizeOpen    = ref(false)
const tailoringMethod  = ref(null)   // 'size' | 'custom'
const liningType       = ref(null)   // 'yem_roi' | 'lien_ta'
const colorOption      = ref(null)   // 'same' | 'custom_color'
const note             = ref('')

// Reset when product changes
watch(product, () => {
  activeImg.value       = 0
  selectedSize.value    = null
  sizeError.value       = false
  openTab.value         = null
  tailoringMethod.value = null
  liningType.value      = null
  colorOption.value     = null
  note.value            = ''
})

// ── Computed ─────────────────────────────────────────────────────────────
const allSelected = computed(() => {
  const methodOk = tailoringMethod.value === 'custom'
    || (tailoringMethod.value === 'size' && selectedSize.value)
  return methodOk && liningType.value && colorOption.value
})

const displayPrice = computed(() => {
  if (!product.value) return ''
  const max = product.value.price
  const min = product.value.price_min ?? max
  if (allSelected.value || min === max) return formatPrice(max)
  return `${formatPrice(min)} – ${formatPrice(max)}`
})
const displayImages = computed(() => {
  if (!product.value) return []
  const imgs = product.value.images ?? []
  // Pad to 4 slots reusing primary color
  const primary = imgs[0] ?? { color_hex: '#d4c8b0' }
  const shades = [1, 0.8, 0.65, 0.5]
  while (imgs.length < 4) imgs.push({ ...primary })
  return imgs.slice(0, 4)
})

const descriptionParagraphs = computed(() => {
  if (!product.value?.description) return []
  return product.value.description.split('\n\n').filter(Boolean)
})

const tabs = computed(() => {
  if (!product.value) return []
  return [
    { key: 'fabric',   label: 'Chất liệu',          content: product.value.fabric            ?? '—' },
    { key: 'care',     label: 'Hướng dẫn chăm sóc', content: product.value.care_instructions  ?? '—' },
    { key: 'shipping', label: 'Giao hàng & Đổi trả', content: product.value.shipping_info     ?? '—' },
  ]
})

const related = computed(() => {
  if (!product.value) return []
  return allProducts.value
    .filter(p => p.slug !== product.value.slug)
    .slice(0, 4)
})

// ── Helpers ─────────────────────────────────────────────────────────────
function formatPrice(price) {
  return Number(price).toLocaleString('vi-VN') + ' đ'
}

function swatchGradient(hex) {
  if (!hex) return 'linear-gradient(160deg, #ece5d5, #d4c8b0)'
  return `linear-gradient(160deg, ${hex}22 0%, ${hex}55 100%)`
}

function selectSize(size) {
  selectedSize.value   = size
  tailoringMethod.value = 'size'
  sizeError.value      = false
}

function handleAddToCart() {
  if (!tailoringMethod.value || (tailoringMethod.value === 'size' && !selectedSize.value)) {
    sizeError.value = true
    return
  }
  cartStore.addItem(product.value, selectedSize.value)
  justAdded.value = true
  setTimeout(() => { justAdded.value = false }, 2000)
}

function handleRelatedAdd(p) {
  // Quick-add without size (open product page instead)
  window.location.href = `/san-pham/${p.slug}`
}

// ── Size guide data ──────────────────────────────────────────────────────
const sizeGuideRows = [
  { size: '32', chest: '76–80',   waist: '60–64',   hip: '84–88',   height: '150–155' },
  { size: '34', chest: '81–85',   waist: '65–69',   hip: '89–93',   height: '153–158' },
  { size: '36', chest: '86–90',   waist: '70–74',   hip: '94–98',   height: '156–161' },
  { size: '38', chest: '91–95',   waist: '75–79',   hip: '99–103',  height: '158–163' },
  { size: '40', chest: '96–100',  waist: '80–84',   hip: '104–108', height: '160–165' },
  { size: '42', chest: '101–106', waist: '85–90',   hip: '109–114', height: '162–167' },
]

// ── Related carousel ─────────────────────────────────────────────────────
const VISIBLE      = 3
const relatedIndex = ref(0)
const relatedVp    = ref(null)
const relatedItemW = ref(0)
let   relatedTimer = null
let   relatedRO    = null

const relatedTrackStyle = computed(() => ({
  transform:  relatedItemW.value
    ? `translateX(-${relatedIndex.value * relatedItemW.value}px)`
    : 'translateX(0)',
  transition: 'transform .5s cubic-bezier(.25,.46,.45,.94)',
}))

async function calcItemW() {
  await nextTick()
  if (relatedVp.value)
    relatedItemW.value = relatedVp.value.offsetWidth / VISIBLE
}

watch(related, async () => {
  relatedIndex.value = 0
  await calcItemW()
})

const relatedAtStart = computed(() => relatedIndex.value === 0)
const relatedAtEnd   = computed(() => relatedIndex.value >= related.value.length - VISIBLE)

function relatedPrev() {
  if (!relatedAtStart.value) relatedIndex.value--
}
function relatedNext() {
  if (!relatedAtEnd.value) relatedIndex.value++
  else relatedIndex.value = 0  // autoplay quay vòng, nút thì bị disable
}

onMounted(async () => {
  await calcItemW()
  relatedRO = new ResizeObserver(calcItemW)
  if (relatedVp.value) relatedRO.observe(relatedVp.value)
  relatedTimer = setInterval(relatedNext, 15000)
})
onUnmounted(() => {
  clearInterval(relatedTimer)
  relatedRO?.disconnect()
})
</script>

<style scoped>
.product-detail-page {
  min-height: 80vh;
  background: var(--warm-white);
}

/* ── Centered wrapper (giống homepage pattern) ───────────────────────────── */
.pd-wrapper {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 48px;
}

/* ── Breadcrumb ──────────────────────────────────────────────────────────── */
.breadcrumb {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  padding: 16px 0;
  font-family: var(--font-body);
  font-size: 10px;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--warm-white);
}
.breadcrumb a {
  color: var(--text-muted);
  transition: color var(--transition);
}
.breadcrumb a:hover { color: var(--charcoal); }
.sep { opacity: .35; margin: 0 2px; }
.breadcrumb-current { color: var(--charcoal); font-weight: 500; }

/* ── Layout ──────────────────────────────────────────────────────────────── */
.pd-layout {
  display: grid;
  grid-template-columns: 58% 42%;
  align-items: start;
  background: var(--warm-white);
}

/* ── Gallery ─────────────────────────────────────────────────────────────── */
.pd-gallery {
  display: flex;
  gap: 10px;
  padding: 20px 24px 20px 0;
  position: sticky;
  top: 84px;
}

.thumb-strip {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.thumb-btn {
  width: 60px;
  aspect-ratio: 2 / 3;
  border: 1.5px solid var(--border);
  background: none;
  padding: 0;
  cursor: pointer;
  overflow: hidden;
  transition: border-color var(--transition);
}
.thumb-btn.active  { border-color: var(--charcoal); }
.thumb-btn:hover   { border-color: var(--gold); }

.thumb-swatch {
  width: 100%;
  height: 100%;
}

.main-img-wrap {
  flex: 1;
}

.main-img {
  width: 100%;
  aspect-ratio: 2 / 3;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.img-overlay-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  z-index: 1;
  pointer-events: none;
}
.overlay-category {
  font-size: 10px;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: rgba(255,255,255,.4);
  font-family: var(--font-body);
}
.overlay-logo {
  font-family: var(--font-display);
  font-size: 80px;
  font-weight: 300;
  letter-spacing: 14px;
  color: rgba(255,255,255,.15);
  line-height: 1;
}
.overlay-logo em { font-style: italic; }

.img-badge {
  position: absolute;
  top: 20px; left: 20px;
  background: var(--charcoal);
  color: var(--cream);
  font-family: var(--font-body);
  font-size: 8px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  padding: 5px 12px;
  z-index: 2;
}

/* ── Info panel ──────────────────────────────────────────────────────────── */
.pd-info {
  padding: 36px 0 48px 40px;
  background: var(--warm-white);
}

.pd-name {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 600;
  letter-spacing: 0.5px;
  line-height: 1.3;
  margin-bottom: 10px;
  color: var(--brand-red);
}

.pd-price {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 400;
  color: var(--brand-red);
  margin-bottom: 28px;
  letter-spacing: 0;
}

/* ── Option sections ─────────────────────────────────────────────────────── */
.pd-option {
  margin-bottom: 20px;
}

.opt-label {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 700;
  color: var(--charcoal);
  margin-bottom: 10px;
}

.opt-sublabel {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 400;
  color: var(--charcoal);
  margin-bottom: 8px;
  display: block;
}

/* Row: sizes trái + "May theo số đo" phải – căn TOP */
.opt-method-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}
.opt-method-left {
  display: flex;
  flex-direction: column;
}

.sizes-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.size-btn {
  min-width: 38px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #C0C0BE;
  background: #fff;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 400;
  color: var(--charcoal);
  cursor: pointer;
  border-radius: 4px;
  transition: all var(--transition);
}
.size-btn:hover:not(.disabled) { border-color: var(--charcoal); }
.size-btn.active {
  background: var(--charcoal);
  border-color: var(--charcoal);
  color: #fff;
}
.size-btn.disabled {
  color: #ccc;
  border-color: #e8e8e6;
  cursor: not-allowed;
  text-decoration: line-through;
}

.method-alt-btn {
  padding: 7px 16px;
  border: 1px solid #C0C0BE;
  background: #fff;
  border-radius: 4px;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 400;
  color: var(--charcoal);
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--transition);
  align-self: flex-start;
}
.method-alt-btn:hover { border-color: var(--charcoal); }
.method-alt-btn.active {
  background: var(--charcoal);
  border-color: var(--charcoal);
  color: #fff;
}

/* Links row */
.opt-links {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}
.opt-links--end { justify-content: flex-end; }
.opt-link {
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 400;
  color: var(--charcoal);
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
  padding: 0;
  transition: color var(--transition);
}
.opt-link:hover { color: var(--brand-red); }

.opt-error {
  font-size: 11px;
  color: #c0395a;
  margin-top: 6px;
}

/* Two-choice button row */
.opt-choice-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.choice-btn {
  padding: 9px 22px;
  border: 1px solid #C0C0BE;
  background: #fff;
  border-radius: 5px;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--charcoal);
  cursor: pointer;
  transition: all var(--transition);
}
.choice-btn:hover { border-color: var(--charcoal); }
.choice-btn.active {
  background: var(--charcoal);
  border-color: var(--charcoal);
  color: #fff;
}

/* ── Note input ──────────────────────────────────────────────────────────── */
.pd-note-wrap { margin: 4px 0 20px; }
.pd-note-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #DDDDD8;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--charcoal);
  background: #fff;
  outline: none;
  transition: border-color var(--transition);
}
.pd-note-input::placeholder { color: #B0B0A8; font-size: 12px; }
.pd-note-input:focus { border-color: #999; }

/* ── Add to cart ─────────────────────────────────────────────────────────── */
.add-to-cart-btn {
  width: 100%;
  padding: 17px;
  background: var(--brand-red);
  border: none;
  border-radius: 0;
  color: #fff;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  cursor: pointer;
  transition: background var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 32px;
}
.add-to-cart-btn:hover { background: var(--brand-dark); }
.add-to-cart-btn.added { background: #2a5a2a; }
.added-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── Accordion ───────────────────────────────────────────────────────────── */
.pd-accordion { margin-top: 8px; }

.accordion-item { border-bottom: none; }

.accordion-trigger {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 10px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--charcoal);
  cursor: pointer;
  text-align: left;
  transition: color var(--transition);
}
.accordion-trigger:hover { color: var(--gold); }

.accordion-icon {
  width: 12px; height: 8px;
  flex-shrink: 0;
  transition: transform var(--transition);
  color: var(--text-muted);
}
.accordion-icon.rotated { transform: rotate(180deg); }

.accordion-body { padding: 0 0 18px; }
.accordion-body p {
  font-family: var(--font-display);
  font-size: 15px;
  font-style: italic;
  line-height: 1.85;
  color: var(--text-muted);
}

.accordion-enter-active, .accordion-leave-active {
  transition: max-height .3s ease, opacity .25s ease;
  overflow: hidden;
  max-height: 300px;
}
.accordion-enter-from, .accordion-leave-to {
  max-height: 0;
  opacity: 0;
}

/* ── Related products carousel ───────────────────────────────────────────── */
.pd-related {
  background: var(--bg-gray);
  border-top: 1px solid var(--border);
}
.pd-related-inner {
  max-width: 1300px;
  margin: 0 auto;
  padding: 64px 48px 72px;
}

.related-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--brand-red);
  margin-bottom: 40px;
}

/* Carousel */
.rel-carousel {
  display: flex;
  align-items: center;
  gap: 20px;
  overflow: hidden; /* catch bất kỳ bleed nào */
}

.rel-viewport {
  flex: 1;
  min-width: 0; /* quan trọng: cho phép flex item shrink đúng */
  overflow: hidden;
}

.rel-track {
  display: flex;
  will-change: transform;
}

.rel-slide {
  flex-shrink: 0;
  flex-grow: 0;
  padding: 0 10px;
  display: block;
  color: inherit;
  text-decoration: none;
  box-sizing: border-box;
}

.rel-img {
  aspect-ratio: 3 / 4;
  overflow: hidden;
  margin-bottom: 16px;
  background: var(--cream-dark);
}

.rel-swatch {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform .55s cubic-bezier(.25,.46,.45,.94);
}
.rel-slide:hover .rel-swatch { transform: scale(1.03); }

.rel-img-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  pointer-events: none;
}
.rel-overlay-sub {
  font-size: 9px;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: rgba(255,255,255,.4);
  font-family: var(--font-body);
}
.rel-overlay-logo {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 300;
  letter-spacing: 10px;
  color: rgba(255,255,255,.15);
  line-height: 1;
}
.rel-overlay-logo em { font-style: italic; }

.rel-info { padding: 0 4px; }

.rel-name {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--charcoal);
  line-height: 1.35;
  margin-bottom: 6px;
  transition: color var(--transition);
}
.rel-slide:hover .rel-name { color: var(--brand-red); }

.rel-price {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--charcoal);
  letter-spacing: 0.3px;
}

/* Arrows */
.rel-arrow {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  background: none;
  border: 1px solid #C8C8C6;
  color: var(--charcoal);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color var(--transition), color var(--transition);
  border-radius: 0;
}
.rel-arrow:hover:not(:disabled) { border-color: var(--charcoal); color: var(--brand-red); }
.rel-arrow:disabled { opacity: .25; cursor: default; }
.rel-arrow svg { width: 20px; height: 20px; }

/* ── Skeleton ────────────────────────────────────────────────────────────── */
.pd-skeleton {
  display: grid;
  grid-template-columns: 55% 45%;
  min-height: 80vh;
}
.skeleton-gallery {
  display: flex;
  gap: 10px;
  padding: 28px 16px 28px 48px;
}
.skeleton-thumb-col {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.skeleton-thumb {
  width: 60px;
  height: 76px;
  background: var(--cream-dark);
  animation: shimmer 1.5s ease infinite;
}
.skeleton-main-img {
  flex: 1;
  background: var(--cream-dark);
  animation: shimmer 1.5s ease infinite;
}
.skeleton-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 40px 48px 40px 36px;
}
.skeleton-line {
  height: 14px;
  background: var(--cream-dark);
  border-radius: 2px;
  animation: shimmer 1.5s ease infinite;
}
.skeleton-line.tall  { height: 32px; }
.skeleton-line.w-30  { width: 30%; }
.skeleton-line.w-40  { width: 40%; }
.skeleton-line.w-60  { width: 60%; }
.skeleton-line.w-70  { width: 70%; }
.skeleton-line.w-full { width: 100%; }

@keyframes shimmer {
  0%, 100% { opacity: 1; }
  50%       { opacity: .5; }
}

/* ── Error ───────────────────────────────────────────────────────────────── */
.pd-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  gap: 16px;
  color: var(--text-muted);
}
.back-link {
  font-family: var(--font-body);
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  border-bottom: 1px solid var(--charcoal);
  padding-bottom: 2px;
  color: var(--charcoal);
  transition: color var(--transition);
}
.back-link:hover { color: var(--gold); }

/* ── Modal ───────────────────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26,26,24,.5);
  z-index: 1200;
  backdrop-filter: blur(2px);
}
.modal {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 680px;
  max-width: calc(100vw - 32px);
  background: var(--warm-white);
  z-index: 1201;
  max-height: 80vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px 20px;
  border-bottom: 1px solid var(--border);
}
.modal-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--charcoal);
}
.modal-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-muted);
  line-height: 1;
  transition: color var(--transition);
}
.modal-close:hover { color: var(--charcoal); }
.modal-body { padding: 28px 32px; }

.size-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.size-table th, .size-table td {
  text-align: center;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}
.size-table th {
  font-family: var(--font-body);
  font-size: 9px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--cream-dark);
  font-weight: 600;
}
.size-table tr:hover td { background: var(--cream); }
.size-note {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 16px;
  line-height: 1.6;
  font-style: italic;
}

.overlay-enter-active, .overlay-leave-active { transition: opacity .3s; }
.overlay-enter-from,   .overlay-leave-to     { opacity: 0; }
.modal-enter-active, .modal-leave-active {
  transition: opacity .3s ease, transform .3s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: translate(-50%, -46%);
}
</style>
