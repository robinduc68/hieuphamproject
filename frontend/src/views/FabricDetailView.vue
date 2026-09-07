<template>
  <div class="fd-page">
    <div v-if="!fabric" class="fd-error">
      <p>Không tìm thấy mẫu vải.</p>
      <RouterLink :to="basePath" class="back-link">← Về kho lụa</RouterLink>
    </div>

    <template v-else>
      <div class="fd-wrapper">
        <!-- Breadcrumb -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <RouterLink to="/">Home Page</RouterLink>
          <span class="sep">/</span>
          <RouterLink :to="basePath">Kho lụa</RouterLink>
          <span class="sep">/</span>
          <span class="breadcrumb-current">{{ fabric.name }}</span>
        </nav>

        <div class="fd-layout">
          <!-- Gallery -->
          <div class="fd-gallery">
            <div class="thumb-strip">
              <button
                v-for="i in 3"
                :key="i"
                class="thumb-btn"
                :class="{ active: activeImg === i - 1 }"
                @click="activeImg = i - 1"
              >
                <span class="thumb-swatch" :style="{ background: grad }" />
              </button>
            </div>
            <div class="main-img" :style="{ background: grad }">
              <span class="main-shimmer" />
            </div>
          </div>

          <!-- Info -->
          <div class="fd-info">
            <h1 class="fd-name">{{ fabric.name }}</h1>
            <p class="fd-price">{{ formatPrice(fabric.price) }}</p>
            <p class="fd-unit"><em>Đơn giá trên 1 mét vải (chiều dài)</em></p>

            <ul class="fd-specs">
              <li>Mã sản phẩm: {{ fabric.code }}</li>
              <li>Chất liệu: Lụa tơ tằm Nha Xá - Hàng loại 1</li>
              <li v-if="isPureSilk">Quy cách: 100% Tơ Tằm (Chi Số Tơ 32-33)</li>
              <li v-else>Quy cách: 70% Tơ Tằm &amp; 30% Tơ Rayon Viscose (Chi Số Tơ 32-33)</li>
              <li>Khổ vải: 90cm</li>
            </ul>

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

          </div>
        </div>

        <!-- Thông tin mẫu vải: card có tab ở header -->
        <section class="fd-info-card">
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
          <div class="fd-info-body" role="tabpanel">
            <p>{{ tabs.find(t => t.key === openTab)?.content }}</p>
          </div>
        </section>
      </div>

      <!-- Related fabrics -->
      <section class="fd-related">
        <div class="fd-related-inner">
          <h2 class="related-title">SẢN PHẨM LIÊN QUAN</h2>
          <div class="related-grid">
            <RouterLink
              v-for="f in related"
              :key="f.id"
              :to="`${basePath}/${f.id}`"
              class="rel-card"
            >
              <div class="rel-img" :style="{ background: fabricGradient(f.color1, f.color2) }" />
              <p class="rel-name">{{ f.name }}</p>
            </RouterLink>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getFabric, collectionOf, pureSilkFabrics, fabricGradient } from '@/data/fabrics'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const cart  = useCartStore()

const fabric   = computed(() => getFabric(route.params.id))
const grad     = computed(() => fabric.value ? fabricGradient(fabric.value.color1, fabric.value.color2) : '')
const activeImg = ref(0)
const qty      = ref(1)
const justAdded = ref(false)
const openTab  = ref('desc')

watch(() => route.params.id, () => { activeImg.value = 0; qty.value = 1; openTab.value = 'desc' })

const tabs = computed(() => [
  { key: 'desc',  label: 'Mô tả', content: `Lụa tơ tằm Nha Xá dệt thủ công, họa tiết ${fabric.value?.pattern}. Chất vải mềm mượt, óng ả, thoáng mát, phù hợp may áo dài, pháp phục và trang phục truyền thống.` },
  { key: 'care',  label: 'Hướng dẫn chăm sóc', content: 'Giặt tay với nước lạnh, không dùng chất tẩy mạnh. Phơi trong bóng râm, ủi ở nhiệt độ thấp mặt trái vải.' },
  { key: 'ship',  label: 'Giao hàng & Đổi trả', content: 'Giao hàng toàn quốc 2-5 ngày. Đổi trả trong 7 ngày với vải chưa cắt, còn nguyên tem mác.' },
])

const isPureSilk = computed(() =>
  pureSilkFabrics.some(f => String(f.id) === String(route.params.id))
)
const basePath = computed(() =>
  isPureSilk.value ? '/lua-nha-xa-100-to-tam' : '/lua-to-tam'
)

const related = computed(() =>
  collectionOf(route.params.id).filter(f => f.id !== fabric.value?.id).slice(0, 4)
)

function formatPrice(p) {
  return Number(p).toLocaleString('vi-VN') + ' đ'
}

function addToCart() {
  if (!fabric.value) return
  cart.addItem(
    {
      id:     'fabric-' + fabric.value.id,
      slug:   `${basePath.value.slice(1)}/${fabric.value.id}`,
      name:   fabric.value.name,
      price:  fabric.value.price,
      images: [{ color_hex: fabric.value.color1 }],
    },
    `${qty.value} mét`,
    qty.value,
  )
  justAdded.value = true
  setTimeout(() => { justAdded.value = false }, 2000)
}
</script>

<style scoped>
.fd-page {
  min-height: 80vh;
  background: var(--warm-white);
  padding-top: 100px;
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
.main-img {
  flex: 1; aspect-ratio: 1 / 1; border-radius: 6px; position: relative; overflow: hidden;
}
.main-shimmer {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.25) 50%, rgba(255,255,255,0) 60%);
}

/* Info */
.fd-info { padding: 12px 0 48px; }
.fd-name {
  font-family: var(--font-display); font-size: 30px; font-weight: 600;
  color: var(--brand-red); line-height: 1.25; margin-bottom: 12px;
  text-transform: uppercase;
}
.fd-price { font-family: var(--font-display); font-size: 22px; color: var(--brand-red); margin-bottom: 4px; }
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

.fd-buy { display: flex; gap: 14px; margin-bottom: 40px; }
.qty-stepper {
  display: flex; align-items: center; border: 1px solid var(--border); border-radius: 4px; flex-shrink: 0;
}
.qty-btn {
  width: 40px; height: 48px; background: none; border: none;
  font-size: 18px; color: var(--charcoal); cursor: pointer;
}
.qty-val { width: 40px; text-align: center; font-family: var(--font-body); font-size: 14px; }

.add-to-cart-btn {
  flex: 1; background: var(--brand-red); border: none; color: #fff;
  font-family: var(--font-body); font-size: 12px; font-weight: 600;
  letter-spacing: 3px; cursor: pointer; transition: background var(--transition);
}
.add-to-cart-btn:hover { background: var(--brand-dark); }
.add-to-cart-btn.added { background: #2a5a2a; }

/* Card thông tin (tab ở header) */
.fd-info-card {
  margin: 48px 0 8px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.fd-info-tabs {
  display: flex;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--border);
  background: var(--warm-white, #faf8f5);
}
.fd-info-tab {
  flex: 0 0 auto;
  padding: 18px 28px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: var(--text-muted);
  cursor: pointer;
  white-space: nowrap;
  transition: color var(--transition), border-color var(--transition), background var(--transition);
}
.fd-info-tab:hover { color: var(--text-dark); }
.fd-info-tab.active {
  color: var(--brand-red);
  border-bottom-color: var(--brand-red);
  background: #fff;
}
.fd-info-body { padding: 28px 32px 32px; }
.fd-info-body p {
  font-family: var(--font-display);
  font-size: 16px;
  line-height: 1.9;
  color: var(--text-dark);
}

@media (max-width: 640px) {
  .fd-info-tabs { overflow-x: auto; flex-wrap: nowrap; }
  .fd-info-tab  { padding: 15px 18px; font-size: 12px; }
  .fd-info-body { padding: 22px 20px 26px; }
}

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
  transition: transform var(--transition), box-shadow var(--transition);
}
.rel-card:hover .rel-img { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.15); }
.rel-name {
  font-family: var(--font-body); font-size: 12px; font-weight: 600;
  letter-spacing: .5px; text-align: center; text-transform: uppercase; color: var(--charcoal);
}

.fd-error {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 50vh; gap: 16px; color: var(--text-muted);
}
.back-link {
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  border-bottom: 1px solid var(--charcoal); color: var(--charcoal); padding-bottom: 2px;
}

@media (max-width: 860px) {
  .fd-layout { grid-template-columns: 1fr; }
  .related-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
