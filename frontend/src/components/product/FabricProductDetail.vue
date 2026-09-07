<template>
  <div class="fd-page">
    <div class="fd-wrapper">
      <!-- Breadcrumb -->
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <RouterLink to="/">Home Page</RouterLink>
        <span class="sep">/</span>
        <RouterLink v-if="product.category" :to="`/danh-muc/${product.category.slug}`">
          {{ product.category.name }}
        </RouterLink>
        <span v-if="product.sub_category" class="sep">/</span>
        <span v-if="product.sub_category">{{ product.sub_category }}</span>
        <span class="sep">/</span>
        <span class="breadcrumb-current" aria-current="page">{{ product.name }}</span>
      </nav>

      <div class="fd-layout">
        <!-- Gallery -->
        <div class="fd-gallery">
          <div class="thumb-strip" v-if="images.length > 1">
            <button
              v-for="(img, i) in images"
              :key="img.id ?? i"
              class="thumb-btn"
              :class="{ active: activeImg === i }"
              :aria-label="`Xem ảnh ${i + 1}`"
              @click="activeImg = i"
            >
              <span class="thumb-swatch" :style="{ background: swatchGradient(img.color_hex) }">
                <img v-if="!isPlaceholderImg(img)" :src="img.url" :alt="img.alt_text || product.name" class="thumb-photo" />
              </span>
            </button>
          </div>

          <div class="main-img" :style="{ background: swatchGradient(images[activeImg]?.color_hex) }">
            <img
              v-if="!isPlaceholderImg(images[activeImg])"
              :src="images[activeImg].url"
              :alt="images[activeImg].alt_text || product.name"
              class="main-photo"
            />
            <span v-else class="main-shimmer" aria-hidden="true" />
            <span v-if="product.is_new" class="img-badge">New</span>
          </div>
        </div>

        <!-- Info -->
        <div class="fd-info">
          <h1 class="fd-name">{{ product.name }}</h1>
          <p class="fd-price">
            {{ formatPrice(product.price) }}
            <span v-if="hasDiscount" class="fd-price-old">{{ formatPrice(product.compare_at_price) }}</span>
          </p>
          <p class="fd-unit"><em>Đơn giá trên 1 {{ unit }} vải (chiều dài)</em></p>

          <ul class="fd-specs" v-if="specs.length">
            <li v-for="s in specs" :key="s.label">{{ s.label }}: {{ s.value }}</li>
          </ul>

          <div class="fd-links">
            <button class="fd-link" @click="guideOpen = true">Định mức may đo</button>
          </div>

          <div class="fd-buy">
            <div class="qty-stepper">
              <button class="qty-btn" @click="qty > 1 && qty--" aria-label="Giảm">−</button>
              <span class="qty-val">{{ qty }}</span>
              <button class="qty-btn" @click="qty++" aria-label="Tăng">+</button>
            </div>
            <button class="add-to-cart-btn" :class="{ added: justAdded }" @click="addToCart">
              <span v-if="!justAdded">THÊM VÀO GIỎ HÀNG</span>
              <span v-else>ĐÃ THÊM VÀO GIỎ</span>
            </button>
          </div>

          <p class="fd-total">
            Tạm tính {{ qty }} {{ unit }}: <strong>{{ formatPrice(Number(product.price) * qty) }}</strong>
          </p>
        </div>
      </div>

      <!-- Thông tin mẫu vải: card có tab ở header -->
      <section v-if="tabs.length" class="fd-info-card">
        <div class="fd-info-tabs" role="tablist">
          <button
            v-for="t in tabs"
            :key="t.key"
            class="fd-info-tab"
            :class="{ active: openTab === t.key }"
            role="tab"
            :aria-selected="openTab === t.key"
            @click="openTab = t.key"
          >{{ t.label }}</button>
        </div>
        <!-- Nội dung soạn ở trang admin (đã lọc HTML trong renderRichText) -->
        <div class="fd-info-body rich-text" role="tabpanel" v-html="activeTabHtml" />
      </section>
    </div>

    <!-- Sản phẩm liên quan -->
    <section v-if="related.length" class="fd-related">
      <div class="fd-related-inner">
        <h2 class="related-title">SẢN PHẨM LIÊN QUAN</h2>
        <div class="related-grid">
          <RouterLink
            v-for="p in related"
            :key="p.id"
            :to="`/san-pham/${p.slug}`"
            class="rel-card"
          >
            <div class="rel-img" :style="{ background: swatchGradient(p.images?.[0]?.color_hex) }">
              <img v-if="!isPlaceholderImg(p.images?.[0])" :src="p.images[0].url" :alt="p.name" class="rel-photo" />
            </div>
            <p class="rel-name">{{ p.name }}</p>
            <p class="rel-price">{{ formatPrice(p.price) }}</p>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Định mức may đo — nội dung admin sửa ở trang admin → Nội dung web -->
    <GuideModal
      v-model="guideOpen"
      :title="guide.title" :note="guide.note"
      :columns="guide.columns" :rows="guide.rows"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useCartStore } from '@/stores/cart'
import { renderRichText, richTextToPlain } from '@/utils/richtext'
import { useSiteSettings, guideTable } from '@/composables/useSiteSettings'
import GuideModal from '@/components/ui/GuideModal.vue'

const props = defineProps({
  product: { type: Object, required: true },
  related: { type: Array, default: () => [] },
})

const cart = useCartStore()

const activeImg = ref(0)
const qty       = ref(1)
const justAdded = ref(false)
const openTab   = ref('desc')
const guideOpen = ref(false)

// Bảng định mức may đo: admin sửa ở trang admin → Nội dung web, dưới đây là
// bản mặc định khi chưa cấu hình.
const { settings } = useSiteSettings()

const GUIDE_FALLBACK = {
  title: 'Định Mức May Đo',
  note: '* Định mức tham khảo với khổ vải 90cm. Số đo lớn hoặc kiểu dáng cầu kỳ có thể cần thêm vải.',
  columns: ['Sản phẩm', 'Chiều cao', 'Định mức vải (mét)'],
  rows: [
    ['Áo dài 2 tà', 'Dưới 1m60',     '2.4 – 2.6'],
    ['Áo dài 2 tà', '1m60 – 1m70',   '2.6 – 2.8'],
    ['Áo dài 4 tà', 'Dưới 1m60',     '2.8 – 3.0'],
    ['Áo dài 4 tà', '1m60 – 1m70',   '3.0 – 3.2'],
    ['Pháp phục',   'Mọi chiều cao', '3.0 – 3.5'],
    ['Quần lụa',    'Mọi chiều cao', '1.6 – 1.8'],
  ],
}

const guide = computed(() => guideTable(settings.value.fabric_tailoring_guide, GUIDE_FALLBACK))

watch(() => props.product?.id, () => {
  activeImg.value = 0
  qty.value       = 1
  openTab.value   = 'desc'
})

const images = computed(() => props.product?.images ?? [])
const unit   = computed(() => props.product?.unit_label?.trim() || 'mét')

const hasDiscount = computed(() => {
  const old = Number(props.product?.compare_at_price ?? 0)
  return old > Number(props.product?.price ?? 0)
})

const specs = computed(() => {
  const p = props.product
  return [
    { label: 'Mã sản phẩm', value: p.sku_code },
    { label: 'Chất liệu',   value: richTextToPlain(p.fabric) },
    { label: 'Quy cách',    value: p.specification },
    { label: 'Khổ vải',     value: p.fabric_width },
  ].filter(s => s.value)
})

const tabs = computed(() => {
  const p = props.product
  return [
    { key: 'desc',     label: 'Mô tả',               content: p.description },
    { key: 'fabric',   label: 'Chất liệu',           content: p.fabric },
    { key: 'care',     label: 'Hướng dẫn chăm sóc',  content: p.care_instructions },
    { key: 'shipping', label: 'Giao hàng & Đổi trả', content: p.shipping_info },
  ].filter(t => t.content)
})

watch(tabs, (list) => {
  if (list.length && !list.some(t => t.key === openTab.value)) openTab.value = list[0].key
}, { immediate: true })

const activeTabHtml = computed(() =>
  renderRichText(tabs.value.find(t => t.key === openTab.value)?.content)
)

function formatPrice(p) {
  return Number(p).toLocaleString('vi-VN') + ' đ'
}

function swatchGradient(hex) {
  if (!hex) return 'linear-gradient(160deg, #ece5d5, #d4c8b0)'
  return `linear-gradient(160deg, ${hex}22 0%, ${hex}55 100%)`
}

function isPlaceholderImg(img) {
  return !img?.url || img.url.includes('/placeholder/')
}

function addToCart() {
  cart.addItem(props.product, `${qty.value} ${unit.value}`, qty.value)
  justAdded.value = true
  setTimeout(() => { justAdded.value = false }, 2000)
}
</script>

<style scoped>
/* Component nằm trong .product-detail-page — phần padding-top tránh header
   đã do view cha lo, ở đây không thêm nữa. */
.fd-page {
  min-height: 80vh;
  background: var(--warm-white);
}
.fd-wrapper { max-width: 1300px; margin: 0 auto; padding: 0 48px; }

.breadcrumb {
  display: flex; align-items: center; flex-wrap: wrap; gap: 6px;
  padding: 16px 0; font-family: var(--font-body);
  font-size: 10px; letter-spacing: 1.8px; text-transform: uppercase;
  color: var(--text-muted);
}
.breadcrumb a { color: var(--text-muted); transition: color var(--transition); }
.breadcrumb a:hover { color: var(--charcoal); }
.sep { opacity: .35; }
.breadcrumb-current { color: var(--charcoal); font-weight: 500; text-transform: uppercase; }

.fd-layout { display: grid; grid-template-columns: 55% 45%; gap: 40px; align-items: start; }

/* Gallery */
.fd-gallery { display: flex; gap: 12px; position: sticky; top: 100px; padding: 12px 0 24px; }
.thumb-strip { display: flex; flex-direction: column; gap: 8px; flex-shrink: 0; }
.thumb-btn {
  width: 64px; aspect-ratio: 3 / 4; padding: 0;
  border: 1.5px solid var(--border); background: none; cursor: pointer; overflow: hidden;
  transition: border-color var(--transition);
}
.thumb-btn.active { border-color: var(--brand-red); }
.thumb-swatch { display: block; width: 100%; height: 100%; }
.thumb-photo { width: 100%; height: 100%; object-fit: cover; display: block; }

.main-img {
  flex: 1; aspect-ratio: 1 / 1; border-radius: 6px; position: relative; overflow: hidden;
}
.main-photo { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.main-shimmer {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.25) 50%, rgba(255,255,255,0) 60%);
}
.img-badge {
  position: absolute; top: 16px; left: 16px; z-index: 2;
  background: var(--charcoal); color: var(--cream);
  font-family: var(--font-body); font-size: 8px; letter-spacing: 2.5px;
  text-transform: uppercase; padding: 5px 12px;
}

/* Info */
.fd-info { padding: 12px 0 48px; }
.fd-name {
  font-family: var(--font-display); font-size: 30px; font-weight: 600;
  color: var(--brand-red); line-height: 1.25; margin-bottom: 12px;
  text-transform: uppercase;
}
.fd-price { font-family: var(--font-display); font-size: 22px; color: var(--brand-red); margin-bottom: 4px; }
.fd-price-old {
  margin-left: 10px; font-size: 15px;
  color: var(--text-muted); text-decoration: line-through;
}
.fd-unit { font-family: var(--font-display); font-size: 15px; color: var(--text-muted); margin-bottom: 28px; }

.fd-specs { list-style: none; margin-bottom: 32px; }
.fd-specs li {
  position: relative; padding-left: 18px; margin-bottom: 10px;
  font-family: var(--font-body); font-size: 14px; color: var(--charcoal); line-height: 1.5;
}
.fd-specs li::before {
  content: ''; position: absolute; left: 2px; top: 9px;
  width: 5px; height: 5px; border-radius: 50%; background: var(--brand-red);
}

.fd-links { display: flex; justify-content: flex-start; margin: -18px 0 26px; }
.fd-link {
  background: none; border: none; padding: 0;
  font-family: var(--font-body); font-size: 12px; color: var(--charcoal);
  text-decoration: underline; text-underline-offset: 2px;
  cursor: pointer; transition: color var(--transition);
}
.fd-link:hover { color: var(--brand-red); }

.fd-buy { display: flex; gap: 14px; margin-bottom: 14px; }
.qty-stepper {
  display: flex; align-items: center; border: 1px solid var(--border);
  border-radius: 4px; flex-shrink: 0; background: #fff;
}
.qty-btn { width: 40px; height: 48px; background: none; border: none; font-size: 18px; color: var(--charcoal); cursor: pointer; }
.qty-val { width: 44px; text-align: center; font-family: var(--font-body); font-size: 14px; }

.add-to-cart-btn {
  flex: 1; background: var(--brand-red); border: none; color: #fff;
  font-family: var(--font-body); font-size: 12px; font-weight: 600;
  letter-spacing: 3px; cursor: pointer; transition: background var(--transition);
}
.add-to-cart-btn:hover { background: var(--brand-dark); }
.add-to-cart-btn.added { background: #2a5a2a; }

.fd-total {
  font-family: var(--font-body); font-size: 13px;
  color: var(--text-muted); margin-bottom: 24px;
}
.fd-total strong { color: var(--charcoal); }

/* Card thông tin (tab ở header) */
.fd-info-card {
  margin: 48px 0 8px;
  background: #fff; border: 1px solid var(--border);
  border-radius: 10px; overflow: hidden;
}
.fd-info-tabs {
  display: flex; flex-wrap: wrap;
  border-bottom: 1px solid var(--border);
  background: var(--warm-white, #faf8f5);
}
.fd-info-tab {
  flex: 0 0 auto; padding: 18px 28px;
  background: none; border: none; border-bottom: 2px solid transparent;
  font-family: var(--font-body); font-size: 13px; font-weight: 600;
  letter-spacing: 1.6px; text-transform: uppercase; color: var(--text-muted);
  cursor: pointer; white-space: nowrap;
  transition: color var(--transition), border-color var(--transition), background var(--transition);
}
.fd-info-tab:hover { color: var(--text-dark); }
.fd-info-tab.active { color: var(--brand-red); border-bottom-color: var(--brand-red); background: #fff; }
.fd-info-body { padding: 28px 32px 32px; }

/* Related */
.fd-related { background: var(--warm-white); }
.fd-related-inner { max-width: 1300px; margin: 0 auto; padding: 40px 48px 72px; }
.related-title {
  font-family: var(--font-display); font-size: 26px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase; color: var(--brand-red); margin-bottom: 32px;
}
.related-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.rel-card { display: block; color: inherit; text-decoration: none; }
.rel-img {
  width: 100%; aspect-ratio: 1 / 1; border-radius: 10px; margin-bottom: 10px;
  position: relative; overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition);
}
.rel-photo { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.rel-card:hover .rel-img { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.15); }
.rel-name {
  font-family: var(--font-body); font-size: 12px; font-weight: 600;
  letter-spacing: .5px; text-align: center; text-transform: uppercase; color: var(--charcoal);
}
.rel-price {
  font-family: var(--font-body); font-size: 12px;
  text-align: center; color: var(--text-muted); margin-top: 4px;
}

/* Modal định mức nằm trong components/ui/GuideModal.vue */

@media (max-width: 860px) {
  .fd-wrapper { padding: 0 20px; }
  .fd-layout { grid-template-columns: 1fr; gap: 20px; }
  .fd-gallery { position: static; }
  .related-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .fd-info-tabs { overflow-x: auto; flex-wrap: nowrap; }
  .fd-info-tab  { padding: 15px 18px; font-size: 12px; }
  .fd-info-body { padding: 22px 20px 26px; }
}
</style>
