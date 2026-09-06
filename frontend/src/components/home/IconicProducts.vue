<template>
  <section class="products-section" id="products">
    <div class="products-head">
      <h2 class="products-heading">ĐƯỢC TIN CHỌN NHIỀU NHẤT</h2>
    </div>

    <div class="carousel-wrap">

      <!-- Arrow left: cao bằng card, nền = màu nền, không shadow/border -->
      <button class="arrow arrow-left" @click="prev" aria-label="Trước">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>

      <!-- Viewport -->
      <div class="viewport" ref="viewportEl">
        <div
          class="track"
          :class="{ 'no-anim': !animate }"
          :style="{ transform: `translateX(-${currentIndex * (itemWidth + GAP)}px)` }"
        >
          <div
            v-for="(product, i) in loopProducts"
            :key="i"
            class="product-card"
            :style="{ width: itemWidth + 'px' }"
          >
            <RouterLink :to="product.slug ? `/san-pham/${product.slug}` : '/cua-hang'" class="card-link">
              <!-- Ảnh hỏng/thiếu vẫn giữ khung màu sản phẩm, không vỡ layout -->
              <div class="card-img" :style="{ background: swatch(product.color) }">
                <img
                  v-if="product.image && !brokenImages[product.image]"
                  :src="product.image"
                  :alt="product.name"
                  @error="brokenImages[product.image] = true"
                />
              </div>
              <div class="card-info">
                <p class="card-name">{{ product.name }}</p>
                <p class="card-price">{{ product.price }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Arrow right -->
      <button class="arrow arrow-right" @click="next" aria-label="Sau">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useInfiniteCarousel } from '@/composables/useInfiniteCarousel'
import { useFeaturedProducts } from '@/composables/useProducts'
import { formatPrice } from '@/utils/price'

// Sản phẩm admin tick "Nổi bật" (API /products/featured).
const { products: featured } = useFeaturedProducts(8)

// Chưa có sản phẩm nổi bật nào → giữ khung mẫu để trang chủ không bị trống.
const PLACEHOLDERS = Array.from({ length: 8 }, (_, i) => ({
  id: `ph-${i + 1}`,
  name: 'TÊN SẢN PHẨM',
  slug: '',
  price: '0.000.000 - 0.000.000 Đ',
  image: null,
  color: null,
}))

const products = computed(() => {
  if (!featured.value.length) return PLACEHOLDERS
  return featured.value.map(p => ({
    id:    p.id,
    name:  p.name?.toUpperCase() ?? '',
    slug:  p.slug,
    price: formatPrice(p.price),
    image: p.images?.[0]?.url || null,
    color: p.images?.[0]?.color_hex || null,
  }))
})

// Ảnh 404 (file placeholder chưa sinh) → chỉ hiện nền màu thay vì icon vỡ
const brokenImages = ref({})

function swatch(hex) {
  if (!hex) return 'linear-gradient(160deg, #ece5d5, #d4c8b0)'
  return `linear-gradient(160deg, ${hex}22 0%, ${hex}55 100%)`
}

// Render 2× để carousel vô tận trượt mượt (real + clone)
const loopProducts = computed(() => [...products.value, ...products.value])

const GAP        = 20
const viewportEl = ref(null)
const itemWidth  = ref(300)

const { currentIndex, animate, next, prev, reset } = useInfiniteCarousel(
  () => products.value.length,
  () => itemWidth.value + GAP
)

// Danh sách đổi (API trả về sau khi mount) → tính lại kích thước & về đầu
watch(products, () => {
  nextTick(update)
  reset()
})

/* Số ảnh hiện cùng lúc (desktop = 4, không bị lấn nửa ảnh) */
function computeVisible() {
  const w = window.innerWidth
  return w > 1100 ? 4 : (w > 700 ? 3 : 2)
}

/* Tính độ rộng 1 ảnh theo CHIỀU RỘNG viewport để vừa đúng N ảnh nguyên */
function update() {
  if (!viewportEl.value) return
  const visible = computeVisible()
  itemWidth.value = Math.floor(
    (viewportEl.value.clientWidth - GAP * (visible - 1)) / visible
  )
}

function onResize() {
  update()
  reset()
}

/* ── Auto-play 15s ── */
let timer = null
function startAuto() {
  clearInterval(timer)
  timer = setInterval(next, 15000)
}

onMounted(() => {
  nextTick(update)
  requestAnimationFrame(update)
  window.addEventListener('resize', onResize)
  startAuto()
})
onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  clearInterval(timer)
})
</script>

<style scoped>
.products-section {
  background: var(--bg-gray);
  padding: 0;              /* bỏ padding – slideshow full bleed */
  padding-bottom: 30px;     /* khoảng trống dưới trước footer */
  display: flex;
  flex-direction: column;
}

.products-head {
  padding: 28px 2.5% 18px;  /* giữ padding ở title */
}

.products-heading {
  font-family: 'Philosopher', sans-serif;
  font-size: 27.9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: var(--brand-red);
}

/* Carousel: [arrow] [viewport] [arrow] – nút cao bằng card, tách rời khỏi ảnh */
.carousel-wrap {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 0;            /* nút chỉ 2.5%, hết chỗ còn lại cho ảnh */
}

.viewport {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.track {
  display: flex;
  gap: 20px;
  transition: transform 0.55s cubic-bezier(.25,.46,.45,.94);
  will-change: transform;
}
.track.no-anim { transition: none; }

/* Product card */
.product-card { flex-shrink: 0; }

.card-link {
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  text-decoration: none;
}

.card-img {
  width: 100%;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  border-radius: 6px;
  background: #e0dbd3;
}
.card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .5s ease;
}
.card-link:hover .card-img img { transform: scale(1.04); }

.card-name  { font-size: 15px; font-weight: 600; color: var(--text-dark); }
.card-price { font-size: 13px; color: var(--brand-red); font-weight: 500; }

/* Arrows – cao bằng card, nền = màu nền trang, KHÔNG shadow/border/radius */
.arrow {
  flex-shrink: 0;
  width: 2.5%;        /* chỉ 2.5% – phần còn lại cho ảnh */
  border-radius: 0;
  background: var(--bg-gray);
  border: none;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--brand-red);
  transition: color var(--transition), transform var(--transition);
}
.arrow:hover {
  color: var(--brand-dark);
}
.arrow:hover svg { transform: scale(1.15); }
.arrow svg { width: 28px; height: 28px; transition: transform var(--transition); }

@media (max-width: 700px) {
  .arrow { width: 8%; }
  .arrow svg { width: 24px; height: 24px; }
}
</style>
